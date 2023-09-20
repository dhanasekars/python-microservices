""" 
Created on : 02/09/23 11:49 am
@author : ds  
"""
import unittest
from unittest.mock import patch, Mock, MagicMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, FastAPI
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.apis.todos import add_todo
from app.data.models import RegistrationRequest, User, Todo, ReturnTodo
from app.apis import todos
import pytest

from app.utils.access_token import verify_token

app_test = FastAPI()
test_client = TestClient(app_test)


def config_app():
    """To include router from other modules"""
    app_test.include_router(todos.router)


config_app()


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


class TestAddTodo:
    """Tests for the add_todo route"""

    # @patch("app.apis.todos.get_db")
    # @patch("app.apis.todos.verify_token")
    def test_add_todo_success(self):
        """Test for the add_todo route"""
        # Create a mock user object for authentication
        mock_user = Mock()
        # mock_verify_token.return_value = User(id=1, username="test_user")
        # mock_verify_token.return_value = mock_user

        response = test_client.post(
            "/todos",
            json={
                "title": "Test Todo",
                "description": "Test Description",
            },
            headers={"Authorization": "Bearer test_token"},
        )

        print(response.json())
