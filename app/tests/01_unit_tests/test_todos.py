""" 
Created on : 02/09/23 11:49 am
@author : ds  
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.data.models import RegistrationRequest, User, ReturnTodo
from app.apis import todos
from app.data.setup import get_db
from app.utils.access_token import verify_token

app_test = FastAPI()
test_client = TestClient(app_test)


def config_app():
    """To include router from other modules"""
    app_test.include_router(todos.router)


config_app()


# ---------------------------mocking dependencies--------------------------------
def override_verify_token(
    token="test_token", db=MagicMock()
):  # pylint: disable=unused-argument
    """Override the verify_token function to return a mock user"""
    current_user = User(id=1, username="test_user")
    return current_user


def override_get_db():
    """Override the get_db function to return a mock session"""
    mock_db_session = Mock()
    return mock_db_session


app_test.dependency_overrides[verify_token] = override_verify_token
app_test.dependency_overrides[get_db] = override_get_db
HEADER = {"Authorization": "Bearer test_token"}


class TestRootRoute:
    """Tests for the root route"""

    def test_read_root(self):
        """Test for the root route"""
        response = test_client.get("/")

        # Check if the response status code is 200 (OK)
        assert response.status_code == 200

        # Check if the response JSON contains the expected message
        assert response.json() == {"message": "Welcome to API Challenge"}


@patch("app.apis.todos.register_new_user")  # Mock the function
class TestRegistration:
    """Tests for the registration route"""

    def test_register_user_success(self, mock_register_new_user):
        """Test for the registration route"""

        # Create a mock user object for registration
        mock_user = RegistrationRequest(
            username="testuser", email="test@example.com", password="TestPass123"
        )

        # Mock the get_db function to return a session
        mock_db_session = Mock()
        override_get_db.return_value = mock_db_session

        # Mock the register_new_user function to return a user
        mock_register_new_user.return_value = mock_user

        # Send a POST request to the registration endpoint
        response = test_client.post("/registration/", json=mock_user.model_dump())

        # Assert that the response is successful and contains the access token
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

        # Assert that the register_new_user function was called with the correct arguments
        mock_register_new_user.assert_called_once()

    def test_register_user_exception(self, mock_register_new_user):
        """Test for the registration route with exception"""
        mock_user = RegistrationRequest(
            username="testuser", email="test@example.com", password="TestPass123"
        )

        # Mock the register_new_user function to raise IntegrityError
        mock_register_new_user.side_effect = IntegrityError(
            "IntegrityError message", params={}, orig=None
        )

        # Send a POST request to the registration endpoint
        response = test_client.post("/registration/", json=mock_user.model_dump())

        # Assert that the response status code is 400 (Bad Request)
        assert response.status_code == 400

        # # Assert that the response contains the expected error detail
        assert "Username or email already exists" in response.json()["detail"]

        # Ensure that the register_new_user function was called
        mock_register_new_user.assert_called_once()


class TestAddTodo(unittest.TestCase):
    """Tests for the add_todo route"""

    @patch("app.apis.todos.ReturnTodo")
    @patch("app.apis.todos.logging")
    def test_add_todo(self, _, mock_return_todo):
        """Test that a user can add a todo item."""
        # Mock the FastAPI request dependencies
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "doneStatus": False,
        }
        expected_return_todo = ReturnTodo(
            id=1,
            title="Test Todo",
            description="Test Description",
            doneStatus=False,
        )
        mock_return_todo.return_value = expected_return_todo

        # Call the endpoint function with mocked dependencies
        response = test_client.post("/todos", json=todo_data, headers=HEADER)
        assert response.status_code == 200
        assert response.json() == expected_return_todo.model_dump()
        mock_return_todo.assert_called_once()

    @patch("app.apis.todos.logging.error")  # Mock the logging.error function
    def test_add_todo_exception(self, _):
        """Test that a user cannot add a todo item with invalid data."""
        # Mock the FastAPI request dependencies
        todo_data = {
            "title": "Test Todo",
            "description": "Test Description",
            "doneStatus": False,
        }

        override_get_db.return_value = Exception("Simulated database error")

        # Call the endpoint function with mocked dependencies and assert the exception
        response = test_client.post(
            "/todos",
            json=todo_data,
            headers={"Authorization": "Bearer test_token"},
        )
        assert response.status_code == 500


class TestGetTodos(unittest.TestCase):
    """Tests for the get_todos route"""

    @patch("app.apis.todos.load_user_todos")
    @patch("app.apis.todos.logging")
    def test_get_2_todo(self, _, mock_load_user_todos):
        """Test that a user can get a list of todo items."""
        expected_return_todos = [
            Mock(id=1, title="Todo 1", description="Description 1"),
            Mock(id=2, title="Todo 2", description="Description 2"),
        ]
        mock_load_user_todos.return_value = expected_return_todos
        response = test_client.get("/todos?page=1&per_page=2", headers=HEADER)
        assert response.status_code == 200
        mock_load_user_todos.assert_called_once()

    def test_get_invalid_query_parameter_page_400(self):
        """Test that a user cannot get a list of todo items with invalid data."""
        response = test_client.get("/todos?page=0&per_page=2", headers=HEADER)
        assert response.status_code == 400
        assert "Invalid query parameter" in response.json()["detail"]

    def test_get_invalid_query_parameter_per_page_422(self):
        """Test that a user cannot get a list of todo items with invalid data."""
        response = test_client.get("/todos?page=2&per_page=abc", headers=HEADER)
        assert response.status_code == 422
        assert "Input should be a valid integer" in response.json()["detail"][0]["msg"]

    @patch("app.apis.todos.logging")
    def test_get_todo_exception(self, _):
        """Test that a user cannot get a list of todo items with invalid data."""
        mock_load_user_todos = Mock(side_effect=Exception("Simulated error"))
        with patch("app.apis.todos.load_user_todos", mock_load_user_todos):
            response = test_client.get("/todos")
        self.assertEqual(
            response.status_code, 500
        )  # Check for 500 Internal Server Error
        self.assertEqual(
            response.json()["detail"],
            "Internal Server Error: Simulated error",
        )
        assert mock_load_user_todos.calledonce()
