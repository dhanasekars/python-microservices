""" 
Created on : 04/09/23 1:08 pm
@author : ds  
"""


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

UUID_REGEX_PATTERN = r"^[0-9a-fA-F]{32}$"
PAYLOAD = {
    "title": "Integration Happy Path.",
    "description": "This is created using automated Integration tests.",
}


def start_app():
    """Start the FastAPI app using Uvicorn."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)


def test_read_root():
    """Test for the root route"""
    response = client.get("/")

    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response JSON
    response_data = response.json()

    # Check if the response message matches the expected message
    expected_message = "Welcome to API Challenge"
    assert "message" in response_data
    assert response_data["message"] == expected_message
