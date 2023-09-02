""" 
Created on : 02/09/23 11:49 am
@author : ds  
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app  # Import your FastAPI app instance
from unittest.mock import patch


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

        with patch("apis.todos.load_list", mock_load_list):
            # Make a request to the `/todos` route
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
        with patch("apis.todos.load_list", mock_load_list):
            # Make a request to the `/todos` route
            response = test_client.get("/todos?page=0&per_page=3")

        # Assert the response
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Page and per_page must be positive integer."
        }

        # Assert that the `load_list()` function was called
        mock_load_list.assert_not_called()

        # Test for invalid per_page
        with patch("apis.todos.load_list", mock_load_list):
            # Make a request to the `/todos` route
            response = test_client.get("/todos?page=1&per_page=-1")

        # Assert the response
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Page and per_page must be positive integer."
        }

        # Assert that the `load_list()` function was called
        mock_load_list.assert_not_called()
