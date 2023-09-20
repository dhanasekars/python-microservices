""" 
Created on : 19/09/23 9:22 am
@author : ds  
"""

import os
from multiprocessing import Process
import pytest

from jose import jwt, JWTError
from fastapi.testclient import TestClient
from main import app

from app.utils.access_token import JWT_SECRET_KEY, ALGORITHM
from app.utils.helper import generate_id
from app.utils.config_manager import config_manager

client = TestClient(app)
config_manager.get_secrets()

username = f"IntegrationTestUser{generate_id()}"
email = f"IntegrationTestUser{generate_id()}@example.com"
PASSWORD = os.getenv("TEST_PASSWORD")


def start_app():
    """Start the FastAPI app using Uvicorn."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)


@pytest.fixture(scope="module", autouse=True)
def setup_teardown_app(request):  # pylint: disable=unused-argument
    """Start the app in a separate process."""
    app_process = Process(target=start_app)
    app_process.start()
    yield client

    app_process.terminate()
    app_process.join()


class TestRegistration:
    """Class to test user registration."""

    @pytest.fixture(scope="class", autouse=True)
    def create_unique_user(self):
        """Test that a user can register."""
        response = client.post(
            "/registration/",
            json={
                "username": username,
                "email": email,
                "password": PASSWORD,
            },
        )
        assert isinstance(response.json(), dict)
        assert response.status_code == 200
        assert "access_token" in response.json()
        access_token = response.json()["access_token"]
        assert isinstance(access_token, str)
        assert len(access_token) > 0
        assert response.json()["token_type"] == "bearer"

        # yield the username, email, and access token to use in the next tests
        yield username, email, access_token

    def test_register_user(self, create_unique_user):
        """Test that a user can register."""
        unique_username, unique_email, generated_access_token = create_unique_user

        assert unique_username is not None
        assert unique_email is not None
        assert generated_access_token is not None
        try:
            # Attempt to decode the access token using the JWT_SECRET_KEY and ALGORITHM
            decoded_token = jwt.decode(
                generated_access_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )

            # If decoding succeeds, it's a valid JWT token
            assert decoded_token is not None
            sub_claim = decoded_token.get("sub")
            # check the 'sub' claim to ensure it matches the registered user's email
            assert sub_claim == username

        except JWTError:
            # If decoding fails, the token is invalid
            pytest.fail("Access token is not a valid JWT token")

    def test_duplicate_email(self, create_unique_user):
        """Test that a user cannot register with a duplicate username."""
        unique_username, unique_email, generated_access_token = create_unique_user

        response = client.post(
            "/registration/",
            json={
                "username": username,
                "email": unique_email,
                "password": PASSWORD,
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username or email already exists"

    def test_duplicate_username(self, create_unique_user):
        """Test that a user cannot register with a duplicate username."""
        unique_username, unique_email, generated_access_token = create_unique_user

        response = client.post(
            "/registration/",
            json={
                "username": unique_username,
                "email": email,
                "password": PASSWORD,
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username or email already exists"

    def test_422_error(self):
        """Test that a user cannot register with a duplicate username."""

        response = client.post(
            "/registration/",
            json={
                "username": "",
                "email": email,
                "password": PASSWORD,
            },
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "String should have at least 8 characters"
        )

    def test_422_for_password_rule_no_caps(self):
        """Test for password rule no caps"""

        response = client.post(
            "/registration/",
            json={
                "username": username,
                "email": email,
                "password": "1233434343434",
            },
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Password must contain at least one uppercase letter"
        )

    def test_422_for_password_rule_no_digit(self):
        """Test for password rule no digit"""
        response = client.post(
            "/registration/",
            json={
                "username": username,
                "email": email,
                "password": "ASDFEGTHYJIOO",
            },
        )
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Password must contain at least one digit"
        )
