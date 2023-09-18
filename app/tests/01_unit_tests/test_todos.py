""" 
Created on : 02/09/23 11:49 am
@author : ds  
"""
from unittest.mock import MagicMock
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from fastapi import HTTPException, FastAPI
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.data.setup import get_db
from app.data.models import RegistrationRequest
from app.apis import todos

app_test = FastAPI()
test_client = TestClient(app_test)


def config_app():
    """To include router from other modules"""
    app_test.include_router(todos.router)


config_app()


@patch("app.apis.todos.register_new_user")  # Mock the function
class TestRegistration:
    """Tests for the registration route"""

    @patch("app.apis.todos.get_db")  # Mock the get_db function separately
    def test_register_user_success(self, mock_get_db, mock_register_new_user):
        """Test for the registration route"""

        # Create a mock user object for registration
        mock_user = RegistrationRequest(
            username="testuser", email="test@example.com", password="TestPass123"
        )

        # Mock the get_db function to return a session
        mock_db_session = Mock()
        mock_get_db.return_value = mock_db_session

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


class TestRootRoute:
    """Tests for the root route"""

    def test_read_root(self):
        """Test for the root route"""
        response = test_client.get("/")

        # Check if the response status code is 200 (OK)
        assert response.status_code == 200

        # Check if the response JSON contains the expected message
        assert response.json() == {"message": "Welcome to API Challenge"}


class TestReadTodos:
    """Tests for the read_todos() route"""

    dummy_data = [
        {
            "id": "1",
            "title": "Todo 1",
            "description": "This is a todo item",
            "doneStatus": False,
        },
        {
            "id": "2",
            "title": "Todo 2",
            "description": "This is another todo item",
            "doneStatus": True,
        },
    ]

    def test_read_todos_valid(self):
        """Test for the read_todos() route"""
        mock_load_list = MagicMock()
        mock_load_list.return_value = self.dummy_data

        with patch("app.apis.todos.load_list", mock_load_list):
            # Make a request to the `/app` route
            response = test_client.get("/todos?page=1&per_page=3")

        # Assert the response
        assert response.status_code == 200
        assert response.json() == self.dummy_data
        # Assert that the `load_list()` function was called
        mock_load_list.assert_called_once()

    def test_read_todos_invalid(self):
        """Test for the read_todos() route with invalid page and per_page"""
        mock_load_list = MagicMock()

        # Test for invalid page
        with patch("app.apis.todos.load_list", mock_load_list):
            # Make a request to the `/app` route
            response = test_client.get("/todos?page=0&per_page=3")

        # Assert the response
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Page and per_page must be positive integer."
        }

        # Assert that the `load_list()` function was NOT called
        mock_load_list.assert_not_called()

        # Test for invalid per_page
        with patch("app.apis.todos.load_list", mock_load_list):
            # Make a request to the `/app` route
            response = test_client.get("/todos?page=1&per_page=-1")

        # Assert the response
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Page and per_page must be positive integer."
        }

        # Assert that the `load_list()` function was NOT called
        mock_load_list.assert_not_called()


class TestAddTodo:
    """Tests for the add_todo() route"""

    def test_add_todo_success(self):
        """Test for the add_todo() route 200"""
        mock_load_list = MagicMock()
        mock_load_list.return_value = []

        # Mock the save_list() function
        mock_save_list = MagicMock()

        # Mock the generate_id() function
        mock_generate_id = MagicMock()
        mock_generate_id.return_value = "1"

        # Patch the load_list(), save_list(), and generate_id() functions
        with patch.object(todos, "load_list", mock_load_list), patch.object(
            todos, "save_list", mock_save_list
        ), patch.object(todos, "generate_id", mock_generate_id):
            # Make a request to the `/app` route
            response = test_client.post("/todos", json={"title": "Todo 1"})

            # Get the JSON response
            json_response = response.json()

        # Assert the response
        assert response.status_code == 200
        assert json_response == {
            "id": "1",
            "title": "Todo 1",
            "description": None,
            "doneStatus": False,
        }

        # Assert that the `load_list()` function was called
        mock_load_list.assert_called_once()

        # Assert that the `save_list()` function was called
        mock_save_list.assert_called_once()

        # Assert that the `generate_id()` function was called
        mock_generate_id.assert_called_once()

    def test_add_todo_invalid_data(self):
        """Test for the add_todo() route with invalid data"""
        mock_load_list = MagicMock()
        mock_load_list.return_value = []

        # Mock the save_list() function
        mock_save_list = MagicMock()

        # Mock the generate_id() function
        mock_generate_id = MagicMock()
        mock_generate_id.return_value = "1"

        # Patch the load_list(), save_list(), and generate_id() functions
        with patch.object(todos, "load_list", mock_load_list), patch.object(
            todos, "save_list", mock_save_list
        ), patch.object(todos, "generate_id", mock_generate_id):
            # Make a request to the `/app` route with invalid data
            response = test_client.post("/todos", json={"title": "     "})

        # Assert the response
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "string_too_short"

        # Assert that the `load_list()` function was not called
        mock_load_list.assert_not_called()

        # Assert that the `save_list()` function was not called
        mock_save_list.assert_not_called()

    def test_add_todo_exception(self):
        """Test for the add_todo() route with exception"""
        mock_load_list = MagicMock()
        mock_load_list.return_value = []

        # Mock the save_list() function
        mock_save_list = MagicMock()
        mock_save_list.side_effect = Exception("An error occurred")

        # Mock the generate_id() function
        mock_generate_id = MagicMock()
        mock_generate_id.return_value = "1"

        # Patch the load_list(), save_list(), and generate_id() functions
        with patch.object(todos, "load_list", mock_load_list), patch.object(
            todos, "save_list", mock_save_list
        ), patch.object(todos, "generate_id", mock_generate_id):
            # Make a request to the `/app` route
            response = test_client.post("/todos", json={"title": "Todo 1"})

        # Assert the response
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error: An error occurred"}

        # Assert that the `load_list()` function was called
        mock_load_list.assert_called_once()

        # Assert that the `save_list()` function was not called
        mock_save_list.assert_called_once()

        # Assert that the `generate_id()` function was called
        mock_generate_id.assert_called_once()


class TestReadTodosByID:
    """Tests for read todo by id route"""

    def test_read_todo_success(self):
        """Test for the read_todo() route"""
        mock_get_todo_details = MagicMock()
        mock_get_todo_details.return_value = {"id": "1", "title": "Todo 1"}

        # Patch the get_todo_details() function
        with patch.object(todos, "get_todo_details", mock_get_todo_details):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.get("/todos/1")

            # Get the JSON response
            json_response = response.json()

        # Assert the response
        assert response.status_code == 200
        assert json_response == {"id": "1", "title": "Todo 1"}

        # Assert that the `get_todo_details()` function was called
        mock_get_todo_details.assert_called_once_with("1")

    def test_read_todo_not_found(self):
        """Test for the read_todo() route with invalid data"""
        mock_get_todo_details = MagicMock()
        mock_get_todo_details.return_value = {"error": "Todo not found"}

        # Patch the get_todo_details() function
        with patch.object(todos, "get_todo_details", mock_get_todo_details):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.get("/todos/1")

            # Get the JSON response
            json_response = response.json()

        # Assert the response
        assert response.status_code == 200
        assert json_response["error"] == "Todo not found"

        # Assert that the `get_todo_details()` function was called
        mock_get_todo_details.assert_called_once_with("1")


class TestDeleteTodoByID:
    """class to test the delete route"""

    def test_delete_todo_success(self):
        """Test for the delete_todo() route"""
        mock_remove_todo = MagicMock()
        mock_remove_todo.return_value = "Item with ID 1 removed"

        # Patch the remove_todo() function
        with patch.object(todos, "remove_todo", mock_remove_todo):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.delete("/todos/1")

        # Assert the response
        assert response.status_code == 200
        assert response.json() == "Item with ID 1 removed"

        # Assert that the `remove_todo()` function was called
        mock_remove_todo.assert_called_once_with("1")

    def test_delete_todo_not_found(self):
        """Test for the delete_todo() route with invalid data"""
        mock_remove_todo = MagicMock()
        mock_remove_todo.side_effect = HTTPException(
            status_code=404, detail="ID not found"
        )

        # Patch the remove_todo() function
        with patch.object(todos, "remove_todo", mock_remove_todo):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.delete("/todos/4")

        # Assert the response
        assert response.status_code == 404
        assert response.json() == {"detail": "ID not found"}

        # Assert that the `remove_todo()` function was called
        mock_remove_todo.assert_called_once_with("4")


class TestUpdateTodo:
    """Tests for the `update_todo()` route"""

    def test_update_todo_success(self):
        """Test for the update_todo() route"""
        mock_update_todo = MagicMock()
        mock_update_todo.return_value = {"title": "Todo 1", "doneStatus": False}

        # Patch the update_todo() function
        with patch.object(todos, "update_todo", mock_update_todo):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.put(
                "/todos/1", json={"title": "Todo 1", "doneStatus": False}
            )

        # Assert the response
        assert response.status_code == 200
        assert response.json() == {"title": "Todo 1", "doneStatus": False}

        # Assert that the `update_todo()` function was called
        mock_update_todo.assert_called_once_with(
            "1", {"description": None, "doneStatus": False, "title": "Todo 1"}
        )

    def test_update_todo_list_error(self):
        """Test that the `update_todo_list()` function handles errors."""

        # Create a mock object for the `update_todo()` function.
        mock_update_todo = MagicMock()
        mock_update_todo.return_value = {"error": "Todo not found"}

        # Patch the update_todo() function
        with patch.object(todos, "update_todo", mock_update_todo):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.put(
                "/todos/1", json={"title": "Todo 1", "doneStatus": False}
            )

            # Assert the expected results.
            assert response.status_code == 200
            assert response.json() == {"error": "Todo not found"}

            mock_update_todo.assert_called_once_with(
                "1", {"description": None, "doneStatus": False, "title": "Todo 1"}
            )

    def test_update_blank_body(self):
        """test update with blank body"""
        mock_update_todo = MagicMock()
        mock_update_todo.return_value = {"error": "Todo not found"}

        # Patch the update_todo() function
        with patch.object(todos, "update_todo", mock_update_todo):
            # Make a request to the `/app/{todo_id}` route
            response = test_client.put("/todos/1", json={})

            # Assert the expected results.
            assert response.status_code == 422
            assert (
                response.json()["detail"][0]["msg"]
                == "Value error, At least one of 'title', 'description', "
                "or 'doneStatus' must have a value"  # noqa: C0301
            )

            mock_update_todo.assert_not_called()
