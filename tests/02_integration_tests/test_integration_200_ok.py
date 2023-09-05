""" 
Created on : 04/09/23 1:08 pm
@author : ds  
"""

from multiprocessing import Process
import pytest
from fastapi.testclient import TestClient
from main import app
import re
from hypothesis import given, strategies as st

client = TestClient(app)

uuid_regex_pattern = r"^[0-9a-fA-F]{32}$"
payload = {
    "title": "Integration Happy Path.",
    "description": "This is created using automated Integration tests.",
}


def start_app():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)


class TestTodoHappyPath:
    @pytest.fixture(scope="module", autouse=True)
    def setup_teardown_app(self, request):
        app_process = Process(target=start_app)
        app_process.start()
        yield client

        app_process.terminate()
        app_process.join()

    @pytest.fixture()
    def generated_uuid(self):
        # create a todo item and capture the generated UUID
        response = client.post("/todos", json=payload)
        assert response.status_code == 200
        todo_data = response.json()
        generated_uuid = todo_data["id"]
        assert todo_data["title"] == payload["title"]
        assert todo_data["description"] == payload["description"]
        assert todo_data["doneStatus"] is False
        assert generated_uuid is not None
        assert re.match(uuid_regex_pattern, generated_uuid)
        assert len(generated_uuid) == 32

        yield generated_uuid

    def test_read_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to API Challenge"}

    def test_create_todo_and_assert_response_details(self, generated_uuid):
        pass

    def test_get_todo_details_using_uuid(self, generated_uuid):
        response = client.get(f"/todos/{generated_uuid}")
        assert response.status_code == 200
        todo_data = response.json()
        assert todo_data["title"] == payload["title"]
        assert todo_data["description"] == payload["description"]
        assert todo_data["id"] == generated_uuid
        assert todo_data["doneStatus"] is False

    def test_get_todo_list(self, generated_uuid):
        response = client.get(f"/todos")
        assert response.status_code == 200
        todo_data = response.json()
        response_length = len(todo_data)
        for item in response.json():
            assert isinstance(item, dict)
            assert "id" in item
            assert "title" in item
            assert "description" in item
            assert "doneStatus" in item
            assert response_length <= 5

    def test_per_page_and_page(self, generated_uuid):
        response = client.get(f"todos?page=1&per_page=1")
        assert response.status_code == 200
        todo_data = response.json()
        response_length = len(todo_data)
        assert isinstance(todo_data, list)
        assert response_length == 1
        assert "id" in todo_data[0]
        assert "title" in todo_data[0]
        assert "description" in todo_data[0]
        assert "doneStatus" in todo_data[0]

    def test_put_updating_a_todo(self, generated_uuid):
        response = client.put(
            f"/todos/{generated_uuid}",
            json={
                "title": "This is updated title.",
                "description": "This is updated description.",
                "doneStatus": True,
            },
        )
        assert response.status_code == 200
        update_response = response.json()
        assert isinstance(update_response, dict)
        assert "success" in update_response
        assert update_response["success"] == f"{generated_uuid} updated successfully."

        # Retrieve updated data and assert for its correctness

        response = client.get(f"/todos/{generated_uuid}")
        todo_data = response.json()
        assert isinstance(todo_data, dict)
        assert len(todo_data) == 4
        assert todo_data["title"] == "This is updated title."
        assert todo_data["description"] == "This is updated description."
        assert todo_data["doneStatus"] is True

    def test_delete_a_todo_item(self, generated_uuid):
        response = client.delete(f"/todos/{generated_uuid}")
        response_data = response.json()
        assert isinstance(response_data, dict)
        assert "detail" in response_data
        assert response_data["detail"] == f"Item with ID {generated_uuid} removed"
