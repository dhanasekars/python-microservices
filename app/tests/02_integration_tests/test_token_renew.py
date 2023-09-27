""" 
Created on : 27/09/23 9:13 am
@author : ds  
"""
import os
from multiprocessing import Process
import pytest

from fastapi.testclient import TestClient

from main import app
from utils.helper import generate_id
from utils.config_manager import config_manager

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


@pytest.fixture(scope="module", autouse=True)
def create_unique_user():
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


class TestRenewToken:
    """Class to test renew token route"""

    def test_renew_token_valid(self, create_unique_user):
        """Test renew token route"""
        unique_username, unique_email, access_token = create_unique_user
        response = client.post(
            "/token-renew/",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert isinstance(response.json(), dict)
        assert response.status_code == 200
        assert "access_token" in response.json()
        access_token = response.json()["access_token"]
        assert isinstance(access_token, str)
        assert len(access_token) > 0
        assert response.json()["token_type"] == "bearer"

    def test_renew_token_invalid(self):
        """Test renew token route"""
        response = client.post(
            "/token-renew/",
            headers={"Authorization": "Bearer fake_token"},
        )
        print(response.json())
        print(response.status_code)
        assert isinstance(response.json(), dict)
        assert response.status_code == 401
        assert "detail" in response.json()
