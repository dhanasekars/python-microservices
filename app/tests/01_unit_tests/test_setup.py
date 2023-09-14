""" 
Created on : 14/09/23 9:12 am
@author : ds  
"""
import json
import unittest
from unittest.mock import mock_open, patch, MagicMock, Mock
from passlib.hash import bcrypt
from fastapi import HTTPException
import pytest
from datetime import datetime, timedelta
from app.data.setup import (
    connect_to_database,
    create_database,
    create_tables,
    get_db,
    Base,
    User,
    create_access_token,
    SessionLocal,
)
from app.utils.config_manager import config_manager


class TestDBConnection(unittest.TestCase):
    """Class to test connect_to_database"""

    @patch("app.data.setup.database_exists")
    @patch("app.data.setup.create_database")
    def test_connect_to_database_creates_database_if_it_does_not_exist(
        self, mock_create_database, mock_database_exists
    ):
        mock_database_exists.return_value = False
        mock_create_database.return_value = True

        connect_to_database()

        mock_create_database.assert_called_once()

    @patch("app.data.setup.database_exists")
    @patch("app.data.setup.create_database")
    def test_connect_to_database_does_not_create_database_if_it_already_exists(
        self, mock_create_database, mock_database_exists
    ):
        mock_database_exists.return_value = True
        mock_create_database.return_value = None

        connect_to_database()

        mock_create_database.assert_not_called()

    @patch("app.data.setup.database_exists")
    @patch("app.data.setup.create_database")
    def test_connect_to_database_handles_exception_from_create_database(
        self, mock_create_database, mock_database_exists
    ):
        mock_database_exists.return_value = False
        mock_create_database.side_effect = Exception("Failed to create database")

        with self.assertRaises(Exception):
            connect_to_database()
        assert mock_create_database.call_count == 1
        assert mock_database_exists.call_count == 1


class TestUserPasswordHashing(unittest.TestCase):
    def test_set_password(self):
        # Create an instance of the User class
        user = User()

        # Set a password
        password = "my_secure_password"
        user.set_password(password)

        # Ensure that the password_hash attribute is not empty
        self.assertIsNotNone(user.password_hash)

        # Verify that the password_hash is a valid hash (e.g., bcrypt hash)
        self.assertTrue(user.verify_password(password))

    def test_set_password_empty(self):
        user = User()

        # Test with an empty password
        password = ""
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)

    def test_set_password_invalid_format(self):
        user = User()

        # Test with a password that doesn't meet requirements (e.g., too short)
        password = "asdf"
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)

    def test_set_password_none(self):
        user = User()

        # Test with None as the password
        password = None
        user.set_password(password)

        # Ensure that the password_hash attribute remains None
        self.assertIsNone(user.password_hash)


class TestUserPasswordVerification(unittest.TestCase):
    def test_verify_password_correct(self):
        # Create a User instance and set a password
        user = User()
        password = "my_secure_password"
        user.set_password(password)

        # Verify the correct password
        self.assertTrue(user.verify_password(password))

    def test_verify_password_incorrect(self):
        # Create a User instance and set a password
        user = User()
        password = "my_secure_password"
        user.set_password(password)

        # Verify an incorrect password
        incorrect_password = "incorrect_password"
        self.assertFalse(user.verify_password(incorrect_password))

    def test_verify_password_empty_hash(self):
        # Create a User instance with no password_hash (e.g., uninitialized or invalid state)
        user = User()

        # Verify any password with an empty hash should return False
        password = "my_secure_password"
        self.assertFalse(user.verify_password(password))


class TestCreateTable(unittest.TestCase):
    """Class to test create_tables"""

    @patch("app.data.setup.Base.metadata.create_all")
    def test_create_tables(self, mock_create_all):
        create_tables(db_engine=MagicMock())
        mock_create_all.assert_called_once()

    @patch("app.data.setup.Base.metadata.create_all")
    def test_create_tables_handles_exception(self, mock_create_all):
        mock_create_all.side_effect = Exception("Failed to create tables")
        with self.assertRaises(Exception):
            create_tables(db_engine=MagicMock())
        mock_create_all.assert_called_once()


@patch("app.data.setup.jwt.encode")
@patch("app.data.setup.SECRET_KEY", "mocked_secret_key")
@patch(
    "app.data.setup.datetime",
    Mock(utcnow=Mock(return_value=datetime(2023, 9, 14, 12, 45, 51, 499491))),
)
class TestCreateAccessToken(unittest.TestCase):
    def test_create_access_token(self, mock_encode):
        # Define test data and parameters
        data = {"user_id": 1, "username": "example_user"}
        expires_delta = timedelta(minutes=10)

        # Mock the jwt.encode function to return a predefined token
        mock_encode.return_value = "mocked_access_token"

        # Call the function to be tested
        access_token = create_access_token(data, expires_delta)

        # Assertions
        self.assertEqual(access_token, "mocked_access_token")

        # Verify that jwt.encode was called with the expected arguments
        mock_encode.assert_called_once_with(
            {
                "user_id": 1,
                "username": "example_user",
                "exp": datetime(2023, 9, 14, 12, 55, 51, 499491),
            },
            "mocked_secret_key",
            algorithm="HS256",
        )

    def test_create_access_token_expired(self, mock_encode):
        mock_encode.return_value = None
        data = {"user_id": 1, "username": "example_user"}
        expires_delta = timedelta(
            minutes=-1
        )  # Negative timedelta for immediate expiration

        # Call the function to be tested
        access_token = create_access_token(data, expires_delta)

        # Ensure that the access_token is None or an empty string, indicating expiration
        self.assertIsNone(access_token)  # or self.assertEqual(access_token, "")
        self.assertTrue(mock_encode.called)


class TestGetDB(unittest.TestCase):
    @patch("app.data.setup.SessionLocal")
    def test_get_db(self, mock_session_local):
        # Mock the SessionLocal class
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Call the function to be tested
        db = get_db()

        # Assertions
        self.assertEqual(db, mock_session)
        mock_session_local.assert_called_once()

        # Verify that the session is closed
        mock_session.close.assert_called_once()
