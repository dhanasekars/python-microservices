""" 
Created on : 18/09/23 5:03 pm
@author : ds  
"""
import unittest
from datetime import timedelta, datetime
from unittest.mock import patch, Mock, MagicMock

import pytest
from fastapi import HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from data.models import User
from utils.access_token import create_access_token, verify_token, renew_access_token


@pytest.fixture(scope="module", autouse=True)
def mock_db_session():
    """Fixture to return a mock database session."""
    return MagicMock(spec=Session)


@patch("utils.access_token.jwt.encode")
@patch("utils.access_token.JWT_SECRET_KEY", "mocked_secret_key")
@patch(
    "utils.access_token.datetime",
    Mock(utcnow=Mock(return_value=datetime(2023, 9, 14, 12, 45, 51, 500))),
)
@patch("utils.access_token.ALGORITHM", "mocked_algorithm")
class TestCreateAccessToken(unittest.TestCase):
    """Class to test create_access_token"""

    def test_create_access_token(self, mock_encode):
        """Test that create_access_token() returns the expected token."""
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
                "exp": datetime(2023, 9, 14, 12, 55, 51, 500),
            },
            "mocked_secret_key",
            algorithm="mocked_algorithm",
        )

    def test_create_access_token_expired(self, mock_encode):
        """Test that create_access_token() returns None if the token has expired."""
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


class TestVerifyToken:
    """Class to test verify_token"""

    @patch("utils.access_token.jwt.decode")
    @patch("utils.access_token.JWT_SECRET_KEY", "mocked_secret_key")
    def test_valid_token(self, mock_decode, mock_db_session):
        """Test that verify_token() returns the expected user."""
        # Mock the behavior of jwt.decode
        mock_decode.return_value = {"sub": "test_user"}

        # Create a mock User object to return from the database query
        mock_user = User(id=1, username="test_user")

        # Mock the behavior of db_fixture.query(...).filter(...).first() to return the mock_user
        mock_db_session.query.return_value.filter.return_value.first.return_value = (
            mock_user
        )

        # Call the verify_token function
        user = verify_token("fake_token", db=mock_db_session)

        # Assert the result
        assert isinstance(user, User)
        assert user.username == "test_user"

        # Verify that jwt.decode was called with the correct arguments
        mock_decode.assert_called_once_with(
            "fake_token", "mocked_secret_key", algorithms=["HS256"]
        )

    @patch("utils.access_token.jwt.decode")
    def test_invalid_user_not_in_db(self, mock_decode, mock_db_session):
        """Test that verify_token() raises an exception if the user is not in the database."""
        mock_decode.return_value = {"sub": "test_user"}

        # Create a mock User object to return from the database query
        mock_user = User(id=1, username="test_user")

        # Mock the behavior of db_fixture.query(...).filter(...).first() to return the mock_user
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(HTTPException) as context:
            verify_token("invalid_token", db=mock_db_session)
        assert context.value.status_code == 401
        assert context.value.detail == "Could not validate credentials"

    @patch("utils.access_token.jwt.decode")
    def test_invalid_username_none_in_token(self, mock_decode, mock_db_session):
        """Test that verify_token() raises an exception if the username is None in the token."""
        mock_decode.return_value = {"sub": None}

        with pytest.raises(HTTPException) as context:
            verify_token("invalid_token", db=mock_db_session)
        assert context.value.status_code == 401
        assert context.value.detail == "Could not validate credentials"

    @patch("utils.access_token.jwt.decode")
    def test_jwt_error(self, mock_decode, mock_db_session):
        """Test that verify_token() raises an exception if the username is None in the token."""
        mock_decode.side_effect = JWTError("JWTError")

        with pytest.raises(HTTPException) as context:
            verify_token("invalid_token", db=mock_db_session)
        assert context.value.status_code == 401
        assert context.value.detail == "Could not validate credentials"


class TestRenewAccessToken(unittest.TestCase):
    """Class to test renew_access_token"""

    def setUp(self):
        self.current_user = Mock(username="testuser")
        self.access_token_expires = timedelta(minutes=15)

    @patch("utils.access_token.create_access_token", return_value="mocked_access_token")
    def test_renew_access_token_success(self, mock_create_access_token):
        """Test that renew_access_token() returns the expected result."""
        result = renew_access_token(self.current_user, self.access_token_expires)

        # Assert that the create_access_token function was called with the correct parameters
        mock_create_access_token.assert_called_once_with(
            data={"sub": "testuser"}, expires_delta=self.access_token_expires
        )

        # Assert the expected result

        assert result == {"access_token": "mocked_access_token", "token_type": "bearer"}

    @patch(
        "utils.access_token.create_access_token", side_effect=Exception("Mocked error")
    )
    def test_renew_access_token_failure(self, mock_create_access_token):
        """Test that renew_access_token() raises an exception if the token cannot be renewed."""
        with self.assertRaises(HTTPException) as exc_context:
            renew_access_token(self.current_user, self.access_token_expires)

        # Assert that the create_access_token function was called with the correct parameters
        mock_create_access_token.assert_called_once_with(
            data={"sub": "testuser"}, expires_delta=self.access_token_expires
        )

        # Assert the expected result
        assert exc_context.exception.status_code == 500
        assert exc_context.exception.detail == "Failed to renew access token"
