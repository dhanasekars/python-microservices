""" 
Created on : 30/08/23 11:34 am
@author : ds  
"""
import unittest
from unittest.mock import patch, Mock, ANY
from fastapi import HTTPException

from utils.helper import load_user_todos, register_new_user, generate_id
from data.models import User


@patch("utils.helper.Session")
class TestLoadUserTodos(unittest.TestCase):
    """Class to test Loader user function"""

    def test_load_user_todos(self, mock_session):
        """Test that load_user_todos() returns the correct todo items for the user."""
        # Create a mock database session
        mock_db_session = Mock()
        mock_session.return_value = mock_db_session

        # Create a mock user and to-do data
        mock_user = Mock()
        mock_user.id = 1
        mock_todo_data = [
            Mock(id=1, title="Todo 1", description="Description 1"),
            Mock(id=2, title="Todo 2", description="Description 2"),
        ]

        # Configure the mock database session to return the mock to-do data
        # pylint: disable=C0301
        (
            mock_db_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all
        ).return_value = mock_todo_data
        # pylint: enable=C0301

        # Call the function under test
        todos = load_user_todos(mock_user, page=1, per_page=5, db=mock_db_session)

        # Assertions
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].id, 1)
        self.assertEqual(todos[1].title, "Todo 2")
        self.assertEqual(todos[1].description, "Description 2")
        assert mock_db_session.query.calledonce()

    def test_load_user_todos_exception(self, mock_session):
        """Test that load_user_todos() raises an HTTPException if an error occurs."""
        mock_db_session = Mock()
        mock_session.return_value = mock_db_session

        # Create a mock user
        mock_user = Mock()
        mock_user.id = 1

        # Configure the mock database session to raise an exception
        mock_db_session.query.side_effect = Exception("Database error")

        # Call the function under test
        with self.assertRaises(HTTPException) as context:
            load_user_todos(mock_user, page=1, per_page=5, db=mock_db_session)

        # Assertions
        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(
            context.exception.detail,
            "Error loading user's to-do list: Database error",
        )


class TestRegisterNewUser(unittest.TestCase):
    """module to test Register new user"""

    def test_register_new_user(self):
        """Test that register_new_user() returns the correct user object."""
        mock_db = Mock()

        # Create mock user data
        mock_user_data = Mock(
            username="testuser123",
            email="test@example.com",
            password="test-password123",
        )

        # Call the function with the mock session and user data
        result = register_new_user(mock_db, mock_user_data)

        # Define a mock User object with the expected attributes
        expected_user = User(
            username="testuser123", email="test@example.com", password_hash=ANY
        )

        # Assert that the mock session methods were called as expected
        mock_db.add.assert_called_once()

        # Check the attributes of the expected and actual User objects
        self.assertEqual(result.username, expected_user.username)
        self.assertEqual(result.email, expected_user.email)
        self.assertEqual(result.password_hash, expected_user.password_hash)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(result)

        # Assert that the return value of the function is not None
        self.assertIsNotNone(result)


class TestGenerateID(unittest.TestCase):
    """module to test UUID generation and uniqueness"""

    def test_generate_id_length(self):
        """Test that generate_id() returns a UUID4 hex string with the correct length."""
        generated_id = generate_id()
        self.assertEqual(len(generated_id), 32)  # A UUID4 hex string has 32 characters

    def test_generate_id_uniqueness(self):
        """Test that generate_id() returns a unique ID."""
        id_list = [generate_id() for _ in range(100)]
        self.assertEqual(len(id_list), len(set(id_list)))  # Check for uniqueness
