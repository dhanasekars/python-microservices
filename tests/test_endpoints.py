""" 
Created on : 22/08/23 6:54 am
@author : ds  
"""
from fastapi.testclient import TestClient
import requests
from tests.sample_data import Todos

from main import app


client = TestClient(app=app)


def test_get_todo_items():
    """test to-do get endpoint"""

    response = client.get("/todos/")
    mocked_response = requests.Response()
    mocked_response.status_code = 200
    # print(f'My assert data is {Todos.todos[:5]}')
    assert response.status_code == 200
    assert response.json() == Todos.todos[:5]
