""" 
Created on : 22/08/23 6:54 am
@author : ds  
"""
from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
import requests
from source.Data.sample_data import Todos

client = TestClient(app=app)


def test_get_todo_items():
    """ test to-do get endpoint"""

    response = client.get('/todos/')
    mocked_response = requests.Response()
    mocked_response.status_code = 200
    print(response.content)
    assert response.status_code == 200
    assert response.json() == Todos.todos
