""" 
Created on : 22/08/23 6:54 am
@author : ds  
"""
from fastapi.testclient import TestClient
import requests
from tests.sample_data import Todos

from main import app


client = TestClient(app=app)
