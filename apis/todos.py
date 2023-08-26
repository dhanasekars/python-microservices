""" 
Created on : 24/08/23 8:39 am
@author : ds  
"""

from typing import Optional, List, Dict

import fastapi
from fastapi import Query, HTTPException
from pydantic import BaseModel, Field
from utils.helper import load_list, save_list, generate_id

router = fastapi.APIRouter()


class TodoItem(BaseModel):
    """Base model for to-do list"""
    title: str
    description: Optional[str] = None
    doneStatus: bool = Field(default=False)


class ReturnTodo(TodoItem):
    id: str


@router.get("/")
async def read_root():
    """ root route"""
    return {"message": "Welcome to API Challenge"}


@router.get("/todos", response_model=List[ReturnTodo])
async def read_todos(
        page: int = Query(default=1, description="Page Number"),
        per_page: int = Query(default=5, description="Items per page"),
):
    """Get list of to-do items"""
    if page < 1 or per_page < 1:
        raise HTTPException(
            status_code=400, detail="Page and per_page must be positive integer."
        )

    skip = (page - 1) * per_page

    return load_list()[skip: skip + per_page]


@router.post("/todos")
async def update_todo(todo: TodoItem):
    try:
        todo = todo.model_dump()
        todo.update(id=generate_id())
        # print(type(todo))
        # print(todo)
        data = load_list()
        data.append(todo)
        save_list(data)
        return todo
    except Exception as e:
        return {"bad": "error goes here: {e}"}


@router.get("/test")
async def playground():
    data = load_list()
    return data
