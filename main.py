""" 
Created on : 18/08/23 8:37 am
@author : ds  
"""
# from typing import Union
from fastapi import FastAPI
from source.Data.sample_data import Todos

app = FastAPI()


@app.get("/")
def read_root():
    """root route"""
    return "Welcome to API Challenge"


@app.get("/todos")
def read_todos():
    """route to list all the todos"""
    return Todos.todos
