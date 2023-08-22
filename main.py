""" 
Created on : 18/08/23 8:37 am
@author : ds  
"""
from typing import Optional, List
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field

from source.Data.sample_data import Todos

app = FastAPI()


class TodoItem(BaseModel):
    """ Base model for to-do list """
    id: int
    title: str
    description: Optional[str] = None
    doneStatus: bool = Field(default=False)


@app.get("/")
async def read_root():
    """root route"""
    return {"message": "Welcome to API Challenge"}


@app.get("/todos", response_model=List[TodoItem])
async def read_todos(
        page: int = Query(default=1, description="Page Number"),
        per_page: int = Query(default=5, description="Items per page"),
):
    """Get list of to-do items"""
    if page < 1 or per_page < 1:
        raise HTTPException(status_code=400, detail="Page and per_page must be positive integer.")

    skip = (page - 1) * per_page
    return Todos.todos[skip: skip + per_page]


if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
