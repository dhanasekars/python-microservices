""" 
Created on : 21/09/23 4:10 pm
@author : ds  
"""
import os
from multiprocessing import Process
from unittest.mock import Mock, MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app
from app.data.setup import get_db
from app.utils.helper import generate_id
from app.utils.config_manager import config_manager

client = TestClient(app)
config_manager.get_secrets()

username = f"IntegrationTestUser{generate_id()}"
email = f"IntegrationTestUser{generate_id()}@example.com"
PASSWORD = os.getenv("TEST_PASSWORD")

# Test data for creating a single todo
single_todo_data = {
    "title": "Integration Test 1",
    "description": "Created during Integration Tests.",
}

# Test data for creating two todos
double_todo_data = [
    {"title": "Integration Test 2", "description": "Created during Integration Tests."},
    {"title": "Integration Test 3", "description": "Created during Integration Tests."},
]


def start_app():
    """Start the FastAPI app using Uvicorn."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)


@pytest.fixture(scope="module")
def db_fixture():
    """Create a new database session for a test."""
    session = get_db()
    yield session
    session.close()


@pytest.fixture(scope="module", autouse=True)
def setup_teardown_app(request):  # pylint: disable=unused-argument
    """Start the app in a separate process."""
    app_process = Process(target=start_app)
    app_process.start()
    yield client

    app_process.terminate()
    app_process.join()


def override_get_db():
    """Override the get_db function to return a mock session"""
    mock_db_session = Mock()
    return mock_db_session


@pytest.fixture(scope="module", autouse=True)
def create_user():
    """Yield new user details."""
    response = client.post(
        "/registration/",
        json={
            "username": username,
            "email": email,
            "password": PASSWORD,
        },
    )
    assert isinstance(response.json(), dict)
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]
    assert isinstance(access_token, str)
    assert len(access_token) > 0
    assert response.json()["token_type"] == "bearer"

    # yield the username, email, and access token to use in the next tests
    yield username, email, access_token


@pytest.fixture(scope="module", autouse=True)
def create_todo(create_user):
    """create todo to use in the next tests"""
    unique_username, unique_email, generated_access_token = create_user
    headers = {"Authorization": f"Bearer {generated_access_token}"}

    # Create a single todo
    response_single = client.post("/todos/", json=single_todo_data, headers=headers)
    assert response_single.status_code == 200
    assert isinstance(response_single.json(), dict)

    responses_double = []
    for todo_data in double_todo_data:
        response_double = client.post("/todos/", json=todo_data, headers=headers)
        assert response_double.status_code == 200
        assert isinstance(response_double.json(), dict)
        responses_double.append(response_double.json())

    # yield the username, email, and access token to use in the next tests
    yield {
        "single": response_single.json(),
        "double": responses_double,
        "headers": headers,
    }


@pytest.fixture(scope="module", autouse=True)
def delete_todo_success(create_todo, create_user):
    """Test that a user can add a todo item."""
    unique_username, unique_email, generated_access_token = create_user
    single_todo = create_todo["single"]
    print(single_todo["id"])
    headers = {"Authorization": f"Bearer {generated_access_token}"}
    response = client.delete(f"/todos/{single_todo['id']}", headers=headers)

    assert response.status_code == 200
    response_data = response.json()
    assert (
        response_data["message"] == f"Todo with ID {single_todo['id']} has been removed"
    )
    yield single_todo["id"], headers


class TestTodos:
    """Class to test todos."""

    def test_add_todo_success(self, create_todo, create_user):
        """Test that a user can add a todo item."""
        unique_username, unique_email, generated_access_token = create_user
        single_todo = create_todo["single"]
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        response = client.post("/todos/", json=single_todo, headers=headers)

        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert "title" in response_data
        assert "description" in response_data
        assert "doneStatus" in response_data
        assert response_data["title"] == single_todo_data["title"]
        assert response_data["description"] == single_todo_data["description"]
        assert response_data["doneStatus"] is False

    def test_add_invalid_token(self):
        """Test that a user cannot add a todo item with an invalid token."""
        headers = {"Authorization": "Bearer Fake_token"}
        # Send a POST request with valid data
        response = client.post("/todos", json=single_todo_data, headers=headers)
        assert response.status_code == 401

    def test_add_todo_422_error(self, create_user):
        """Test that a user cannot add a todo item with invalid data."""
        unique_username, unique_email, generated_access_token = create_user
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        invalid_data = {"title": None, "description": "This is an invalid todo item."}
        response = client.post("/todos", json=invalid_data, headers=headers)

        assert response.status_code == 422

        # Parse the response JSON
        response_data = response.json()

        # Check if the response contains an error message
        assert "detail" in response_data
        expected_error_message = (
            "Input should be a valid string"  # This is the expected error message
        )

        # Check if the error message in the response matches the expected error message
        assert response_data["detail"][0]["msg"] == expected_error_message

    def test_get_todos_success(self, create_user):
        """Test get todos success."""
        unique_username, unique_email, generated_access_token = create_user
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        response = client.get("/todos?page=1&per_page=1", headers=headers)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 1
        assert "id" in response_data[0]
        assert "title" in response_data[0]
        assert "description" in response_data[0]
        assert "doneStatus" in response_data[0]

    def test_get_more_than_one(self, create_todo, create_user):
        """Test get todos success."""
        unique_username, unique_email, generated_access_token = create_user
        double_todos = create_todo["double"]
        print(double_todos)
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        response = client.get("/todos?page=1&per_page=2", headers=headers)

        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert len(response_data) == 2
        assert "id" in response_data[0]
        assert "title" in response_data[0]
        assert "description" in response_data[0]
        assert "doneStatus" in response_data[0]

    def test_invalid_query_parameter_page(self, create_user):
        """Test get todos with invalid query parameter."""
        unique_username, unique_email, generated_access_token = create_user
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        response = client.get("/todos?page=0&per_page=2", headers=headers)
        assert response.status_code == 400
        assert "Invalid query parameter" in response.json()["detail"]

    def test_invalid_query_parameter_per_page(self, create_user):
        """Test get todos with invalid query parameter."""
        unique_username, unique_email, generated_access_token = create_user
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        response = client.get("/todos?page=1&per_page=abc", headers=headers)
        assert response.status_code == 422
        assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]

    def test_get_todo_exception(self, create_user):
        """Test the 500 internal server error."""
        app.dependency_overrides[get_db] = override_get_db
        override_get_db.return_value = Exception("Simulated database error")
        unique_username, unique_email, generated_access_token = create_user
        headers = {"Authorization": f"Bearer {generated_access_token}"}
        # Send a POST request with valid data
        response = client.get("/todos", headers=headers)
        assert response.status_code == 500
        app.dependency_overrides = {}

    def test_get_todo_by_id_success(self, create_todo):
        """Test get todos by id success."""
        single_todo = create_todo["double"][0]
        response = client.get(
            f"/todos/{single_todo['id']}", headers=create_todo["headers"]
        )
        assert response.status_code == 200
        response_data = response.json()[0]
        assert isinstance(response_data, dict)
        assert "id" in response_data
        assert "title" in response_data
        assert "description" in response_data
        assert "doneStatus" in response_data

    def test_get_todo_by_id_404(self, create_todo):
        """Test get todos by id success."""
        single_todo = create_todo["single"]
        response = client.get(
            f"/todos/{single_todo['id']}", headers=create_todo["headers"]
        )
        assert response.status_code == 404
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert response_data["detail"] == f"Todo not found"

    def test_delete_todo_success(self, delete_todo_success):
        """Test that a user can add a todo item."""
        pass

    def test_delete_todo_invalid(self, delete_todo_success):
        """Test that a user can add a todo item."""
        test_id, yielded_headers = delete_todo_success
        response = client.delete(f"/todos/{test_id}", headers=yielded_headers)

        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == f"Todo not found"
