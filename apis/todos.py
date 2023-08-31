""" 
Created on : 24/08/23 8:39 am
@author : ds  
"""

from typing import Optional, List

import fastapi
from fastapi import Query, HTTPException
from pydantic import BaseModel, Field
from utils.todo_helper import (
    load_list,
    save_list,
    generate_id,
    get_todo_details,
    remove_todo,
    update_todo,
)

router = fastapi.APIRouter()


class TodoItem(BaseModel):
    """Base model for to-do list"""

    title: str
    description: Optional[str] = None
    doneStatus: bool = Field(default=False)


class ReturnTodo(TodoItem):
    """extending TodoItem class with UUID"""

    id: str


class UpdateTodo(BaseModel):
    """base model with optional field for updating"""

    title: Optional[str] = None
    description: Optional[str] = None
    doneStatus: Optional[bool] = None


@router.get("/")
async def read_root():
    """root route"""
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

    return load_list()[skip : skip + per_page]


@router.post("/todos")
async def add_todo(todo: TodoItem):
    """This is post route to add a To-do item"""
    try:
        todo = todo.model_dump()
        todo.update(id=generate_id())
        data = load_list()
        data.append(todo)
        save_list(data)
        return todo
    except Exception as e:
        return {"bad": f"error goes here: {e}"}


@router.get("/todos/{todo_id}")
async def read_todo(todo_id):
    """return todo details for a given id"""
    result = get_todo_details(todo_id)
    if "error" in result:
        return {"error": f"{result['error']}"}
    return result


@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id):
    """This is to delete an item"""
    return remove_todo(todo_id)


@router.put("/todos/{todo_id}")
async def update_tod(todo: UpdateTodo, todo_id):
    """This route is to update an item"""
    todo = todo.model_dump()
    return update_todo(todo_id, todo)


@router.get("/playground")
async def playground():
    """a test route to be removed later"""
    data = load_list()
    return data
