""" 
Created on : 02/09/23 11:49 am
@author : ds  
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from fastapi import HTTPException
from unittest.mock import patch

from app.apis import todos
from main import app  # Import your FastAPI app instance


# Create a test client using the TestClient class
# client = TestClient(app)
@pytest.fixture
def test_client():
    """Creates a test client for the API"""
    return TestClient(app)


class TestRootRoute:
    # Define a test function
    def test_read_root(self, test_client: TestClient):
        # Send a GET request to the root endpoint
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

    def test_read_todos_valid(self, test_client: TestClient):
        # mock load_list()
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

    def test_read_todos_invalid(self, test_client: TestClient):
        # mock load_list()
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
    def test_add_todo_success(self, test_client):
        # Mock the load_list() function
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

    def test_add_todo_invalid_data(self, test_client):
        # Mock the load_list() function
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

    def test_add_todo_exception(self, test_client):
        # Mock the load_list() function
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

    def test_read_todo_success(self, test_client):
        # Mock the get_todo_details() function
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

    def test_read_todo_not_found(self, test_client):
        # Mock the get_todo_details() function
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

    def test_delete_todo_success(self, test_client):
        # Mock the remove_todo() function
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

    def test_delete_todo_not_found(self, test_client):
        # Mock the remove_todo() function
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

    def test_update_todo_success(self, test_client):
        # Mock the update_todo() function
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

    def test_update_todo_list_error(self, test_client):
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

    def test_update_blank_body(self, test_client):
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
                == "Value error, At least one of 'title', 'description', or 'doneStatus' must have a value"
            )

            mock_update_todo.assert_not_called()
