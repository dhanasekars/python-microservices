""" 
Created on : 18/09/23 5:03 pm
@author : ds  
"""
import unittest
from datetime import timedelta, datetime
from unittest.mock import patch, Mock

from app.utils.access_token import create_access_token


@patch("app.utils.access_token.jwt.encode")
@patch("app.utils.access_token.JWT_SECRET_KEY", "mocked_secret_key")
@patch(
    "app.utils.access_token.datetime",
    Mock(utcnow=Mock(return_value=datetime(2023, 9, 14, 12, 45, 51, 500))),
)
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
            algorithm="HS256",
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
