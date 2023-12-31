""" 
Created on : 14/09/23 9:12 am
@author : ds  
"""
import unittest
from unittest.mock import patch, MagicMock

from fastapi import HTTPException
from data.setup import (
    connect_to_database,
    create_tables,
    get_db,
    db_name,
)
from data.models import User


class TestDBConnection(unittest.TestCase):
    """class to test database connection connect_to_database()"""

    @patch("data.setup.database_exists")
    @patch("data.setup.create_database")
    @patch("data.setup.logging.info")
    def test_connect_to_database_creates_database_if_it_doesnt_exist(
        self, mock_logging_info, mock_create_database, mock_database_exists
    ):
        """Test that connect_to_database() creates the database if it doesn't exist."""
        mock_database_exists.return_value = False

        # Mock the create_database() function to do nothing
        mock_create_database.return_value = None

        # Call the connect_to_database() function
        connect_to_database()

        # Assert that the create_database() function was called
        mock_create_database.assert_called_once()

        # Assert that the logging.info() function was called with the correct message
        mock_logging_info.assert_called_once_with(
            f"Database '{db_name}' created successfully."
        )

    @patch("data.setup.database_exists")
    @patch("data.setup.create_database")
    @patch("data.setup.logging.info")
    def test_connect_to_database_does_not_create_database_if_it_already_exists(
        self, mock_logging_info, mock_create_database, mock_database_exists
    ):
        """Test that connect_to_database() does not create the database if it already exists."""
        mock_database_exists.return_value = True

        # Mock the create_database() function to do nothing
        mock_create_database.return_value = None

        # Call the connect_to_database() function
        connect_to_database()

        # Assert that the create_database() function was not called
        mock_create_database.assert_not_called()

        # Assert that the logging.info() function was called with the correct message
        mock_logging_info.assert_called_once_with(
            f"Database '{db_name}' already exists."
        )

    @patch("data.setup.database_exists")
    @patch("data.setup.create_database")
    @patch("data.setup.logging.error")
    def test_connect_to_database_handles_exception(
        self, mock_logging_error, mock_create_database, mock_database_exists
    ):
        """Test that connect_to_database() handles an exception."""
        mock_database_exists.return_value = False

        # Mock the create_database() function to raise an Exception
        mock_create_database.side_effect = Exception("Database connection failed.")

        # Assert that the connect_to_database() function throws an HTTPException
        with self.assertRaises(HTTPException):
            connect_to_database()

        # Assert that the logging.error() function was called with the correct message
        mock_logging_error.assert_called_once_with("Error: Database connection failed.")


class TestUserPasswordHashing(unittest.TestCase):
    """Class to test password hashing and verification."""

    def test_set_password(self):
        """Test that the set_password() method sets the password_hash attribute."""
        user = User()

        # Set a password
        password = "my_secure_password"
        user.set_password(password)

        # Ensure that the password_hash attribute is not empty
        self.assertIsNotNone(user.password_hash)

        # Verify that the password_hash is a valid hash (e.g., bcrypt hash)
        self.assertTrue(user.verify_password(password))

    def test_set_password_empty(self):
        """Test with an empty password."""
        user = User()

        # Test with an empty password
        password = ""
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)

    def test_set_password_invalid_format(self):
        """Test with a password that doesn't meet requirements (e.g., no uppercase letter)."""
        user = User()

        # Test with a password that doesn't meet requirements (e.g., too short)
        password = "asdf"
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)

    def test_set_password_none(self):
        """Test with None as the password."""
        user = User()

        # Test with None as the password
        password = None
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)


class TestUserPasswordVerification(unittest.TestCase):
    """Class to test password verification."""

    def test_verify_password_correct(self):
        """Test that the verify_password() method returns True for a correct password."""
        user = User()
        password = "my_secure_password"
        user.set_password(password)

        # Verify the correct password
        self.assertTrue(user.verify_password(password))

    def test_verify_password_incorrect(self):
        """Test that the verify_password() method returns False for an incorrect password."""
        user = User()
        password = "my_secure_password"
        user.set_password(password)

        # Verify an incorrect password
        incorrect_password = "incorrect_password"
        self.assertFalse(user.verify_password(incorrect_password))

    def test_verify_password_empty_hash(self):
        """Test that the verify_password() method returns False for an empty password_hash."""
        user = User()

        # Verify any password with an empty hash should return False
        password = "my_secure_password"
        self.assertFalse(user.verify_password(password))


class TestCreateTable(unittest.TestCase):
    """Class to test create_tables"""

    @patch("data.setup.Base.metadata.create_all")
    def test_create_tables(self, mock_create_all):
        """Test that create_tables() calls Base.metadata.create_all()"""
        create_tables(db_engine=MagicMock())
        mock_create_all.assert_called_once()

    @patch("data.setup.Base.metadata.create_all")
    def test_create_tables_handles_exception(self, mock_create_all):
        """Test that create_tables() handles an exception."""
        mock_create_all.side_effect = Exception("Failed to create tables")
        with self.assertRaises(Exception):
            create_tables(db_engine=MagicMock())
        mock_create_all.assert_called_once()


class TestGetDB(unittest.TestCase):
    """Class to test get_db"""

    @patch("data.setup.SessionLocal")
    def test_get_db(self, mock_session_local):
        """Test that get_db() returns the expected session."""
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Call the function to be tested
        result_db = get_db()

        # Assertions
        self.assertEqual(result_db, mock_session)
        mock_session_local.assert_called_once()

        # Verify that the session is closed
        mock_session.close.assert_called_once()
