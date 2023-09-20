""" 
Created on : 04/09/23 1:08 pm
@author : ds  
"""

from multiprocessing import Process
import re

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

UUID_REGEX_PATTERN = r"^[0-9a-fA-F]{32}$"
PAYLOAD = {
    "title": "Integration Happy Path.",
    "description": "This is created using automated Integration tests.",
}


def start_app():
    """Start the FastAPI app using Uvicorn."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)


class TestTodo2xx:
    """Test class for 2xx status codes"""

    @pytest.fixture(scope="module", autouse=True)
    def setup_teardown_app(self, request):  # pylint: disable=unused-argument
        """Setup and teardown the app"""
        app_process = Process(target=start_app)
        app_process.start()
        yield client

        app_process.terminate()
        app_process.join()

    @pytest.fixture()
    def generated_uuid(self):
        """Create a todo item and capture the generated UUID"""
        response = client.post("/todos", json=PAYLOAD)
        assert response.status_code == 200
        todo_data = response.json()
        generated_uuid = todo_data["id"]
        assert todo_data["title"] == PAYLOAD["title"]
        assert todo_data["description"] == PAYLOAD["description"]
        assert todo_data["doneStatus"] is False
        assert generated_uuid is not None
        assert re.match(UUID_REGEX_PATTERN, generated_uuid)
        assert len(generated_uuid) == 32

        yield generated_uuid

    def test_read_root(self):
        """Test root route"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to API Challenge"}

    def test_create_todo_and_assert_response_details(self, generated_uuid):
        """Test create todo and assert response details"""
        pass

    def test_get_todo_details_using_uuid(self, generated_uuid):
        """Test get todo details using UUID"""
        response = client.get(f"/todos/{generated_uuid}")
        assert response.status_code == 200
        todo_data = response.json()
        assert todo_data["title"] == PAYLOAD["title"]
        assert todo_data["description"] == PAYLOAD["description"]
        assert todo_data["id"] == generated_uuid
        assert todo_data["doneStatus"] is False

    def test_get_todo_list(self, generated_uuid):  # pylint: disable=unused-argument
        """Test get todo list"""
        response = client.get("/todos")
        assert response.status_code == 200
        todo_data = response.json()
        response_length = len(todo_data)
        for item in response.json():
            assert isinstance(item, dict)
            assert "id" in item
            assert "title" in item
            assert "description" in item
            assert "doneStatus" in item
            assert response_length <= 5

    def test_per_page_and_page(self, generated_uuid):  # pylint: disable=unused-argument
        """Test per page and page"""
        response = client.get("todos?page=1&per_page=1")
        assert response.status_code == 200
        todo_data = response.json()
        response_length = len(todo_data)
        assert isinstance(todo_data, list)
        assert response_length == 1
        assert "id" in todo_data[0]
        assert "title" in todo_data[0]
        assert "description" in todo_data[0]
        assert "doneStatus" in todo_data[0]

    def test_put_updating_a_todo(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test put updating a todo"""
        response = client.put(
            f"/todos/{generated_uuid}",
            json={
                "title": "This is updated title.",
                "description": "This is updated description.",
                "doneStatus": True,
            },
        )
        assert response.status_code == 200
        update_response = response.json()
        assert isinstance(update_response, dict)
        assert "success" in update_response
        assert update_response["success"] == f"{generated_uuid} updated successfully."

        # Retrieve updated data and assert for its correctness

        response = client.get(f"/todos/{generated_uuid}")
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert len(todo_data) == 4
        assert todo_data["title"] == "This is updated title."
        assert todo_data["description"] == "This is updated description."
        assert todo_data["doneStatus"] is True

    def test_delete_a_todo_item(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test delete a todo item"""
        response = client.delete(f"/todos/{generated_uuid}")
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "detail" in response_data
        assert response_data["detail"] == f"Item with ID {generated_uuid} removed"


class TestTodo4xx:
    """Test class for 4xx status codes"""

    @pytest.fixture(scope="module", autouse=True)
    def setup_teardown_app(self, request):  # pylint: disable=unused-argument
        """Setup and teardown the app"""
        app_process = Process(target=start_app)
        app_process.start()
        yield client

        app_process.terminate()
        app_process.join()

    @pytest.fixture()
    def generated_uuid(self):
        """Create a todo item and capture the generated UUID"""
        response = client.post("/todos", json=PAYLOAD)
        assert response.status_code == 200
        todo_data = response.json()
        generated_uuid = todo_data["id"]
        assert todo_data["title"] == PAYLOAD["title"]
        assert todo_data["description"] == PAYLOAD["description"]
        assert todo_data["doneStatus"] is False
        assert generated_uuid is not None
        assert re.match(UUID_REGEX_PATTERN, generated_uuid)
        assert len(generated_uuid) == 32

        yield generated_uuid

    def test_pagination_page_less_than_one(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test pagination page less than one"""
        response = client.get("todos?page=0&per_page=1")
        assert response.status_code == 400
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert todo_data["detail"] == "Page and per_page must be positive integer."

    def test_pagination_per_page_less_than_one(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test pagination per page less than one"""
        response = client.get("todos?page=1&per_page=0")
        assert response.status_code == 400
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert todo_data["detail"] == "Page and per_page must be positive integer."

    def test_pagination_422(self, generated_uuid):  # pylint: disable=unused-argument
        """Test pagination 422"""
        response = client.get("todos?page=notNumber&per_page=1")
        assert response.status_code == 422
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert (
            todo_data["detail"][0]["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
        )

    def test_get_invalid_todo(self):
        """Test get invalid todo"""
        response = client.get("/todos/aninvalidID123")
        assert response.status_code == 404
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert todo_data["detail"] == "Todo not found for the given ID: aninvalidID123"

    def test_update_invalid_todo(self):
        """Test update invalid todo"""
        response = client.put(
            "/todos/aninvalidID123", json={"title": "Update invalid id"}
        )
        assert response.status_code == 404
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert todo_data["detail"] == "aninvalidID123 not found."

    def test_delete_invalid_todo(self):
        """Test delete invalid todo"""
        response = client.delete("/todos/aninvalidID123")
        assert response.status_code == 404
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert "detail" in todo_data
        assert todo_data["detail"] == "ID not found"

    def test_update_with_blank_422(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test update with blank 422"""
        response = client.put(
            f"/todos/{generated_uuid}",
            json={
                "title": " ",
                "description": "This is updated description.",
                "doneStatus": True,
            },
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "string_too_short"

    def test_post_todo_with_blank_422(
        self, generated_uuid
    ):  # pylint: disable=unused-argument
        """Test post todo with blank 422"""
        response = client.post(
            "/todos",
            json={
                "title": " ",
                "description": "This is updated description.",
                "doneStatus": True,
            },
        )
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "string_too_short"


class TestTodo5xx:
    """Test class for 5xx status codes"""

    @pytest.fixture(scope="module", autouse=True)
    def setup_teardown_app(self, request):  # pylint: disable=unused-argument
        """Setup and teardown the app"""
        app_process = Process(target=start_app)
        app_process.start()
        yield client

        app_process.terminate()
        app_process.join()

    @pytest.fixture()
    def generated_uuid(self):
        """Create a todo item and capture the generated UUID"""
        # create a todo item and capture the generated UUID
        response = client.post("/todos", json=PAYLOAD)
        assert response.status_code == 200
        todo_data = response.json()
        generated_uuid = todo_data["id"]
        assert todo_data["title"] == PAYLOAD["title"]
        assert todo_data["description"] == PAYLOAD["description"]
        assert todo_data["doneStatus"] is False
        assert generated_uuid is not None
        assert re.match(UUID_REGEX_PATTERN, generated_uuid)
        assert len(generated_uuid) == 32

        yield generated_uuid

    def test_internal_server_error(self):
        """Test internal server error"""

        # Define a function to mock the route handler and raise an exception
        def mock_route_handler(_, __):
            """Mock route handler to raise an exception"""
            raise Exception("Simulated internal server error")

        # Use the monkeypatch fixture to replace the route handler with the mock function
        with pytest.raises(Exception):
            client.app.router.routes[0].endpoint = mock_route_handler

            # Send a POST request to trigger the route
            response = client.post("/todos", json={"title": "Test Todo"})
            print(response.json())
            # Verify that the response status code is 500
            assert response.status_code == 500
