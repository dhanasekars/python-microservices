""" 
Created on : 24/08/23 8:39 am
@author : ds  
"""
from typing import List
from datetime import timedelta
import logging
import fastapi
from fastapi import Query, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utils.access_token import create_access_token, verify_token
from app.utils.helper import (
    register_new_user,
    load_user_todos,
)
from app.utils.config_manager import config_manager
from app.data.models import (
    ReturnTodo,
    TodoItem,
    RegistrationRequest,
    User,
    Todo,
)
from app.data.setup import get_db
from app.utils.custom_exceptions import InvalidQueryParameter

router = fastapi.APIRouter()

# Configure logging
config_manager.configure_logging()
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    config_manager.config_data["authentication"]["token_expiry"]
)  # 2 weeks


@router.get("/")
async def read_root():
    """root route"""
    logging.info("Request received at root route.")
    return {"message": "Welcome to API Challenge"}


# Registration endpoint
@router.post("/registration/")
def register_user(user: RegistrationRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        db_user = register_new_user(db, user)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    except IntegrityError as err:
        db.rollback()
        logging.error(f"Error: {err}")
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.post("/todos")
async def add_todo(
    todo: TodoItem,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),  # Add user authentication dependency
):
    """This is a post route to add a To-do item"""
    try:
        logging.debug("Adding a new todo item")
        # Create a new Todo object and associate it with the current user
        new_todo = Todo(
            title=todo.title, description=todo.description, owner=current_user
        )

        # Add the new todo to the database
        db.add(new_todo)
        db.commit()

        # Refresh and Return the added todo
        db.refresh(new_todo)
        return_todo = ReturnTodo(
            id=new_todo.id,
            title=new_todo.title,
            description=new_todo.description,
            doneStatus=new_todo.status,
        )

        return return_todo

    except Exception as err:
        error_message = f"Internal Server Error: {err}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.get("/todos", response_model=List[ReturnTodo])
async def get_todos(
    page: int = Query(default=1, description="Page Number"),
    per_page: int = Query(default=5, description="Items per page"),
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """This is a get route to get all the To-do items"""
    if page < 1 or per_page < 1:
        raise InvalidQueryParameter()  # Raise the custom exception
    # Otherwise, retrieve a list of todo items for the current user.
    try:
        todos = load_user_todos(current_user, page, per_page, db)
        return_todos = [ReturnTodo(**todo.__dict__) for todo in todos]
        return return_todos
    except Exception as err:
        error_message = f"Internal Server Error: {err}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.get("/todos/{todo_id}", response_model=List[ReturnTodo])
async def get_todo_by_id(
    todo_id: int,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """This is a get route to get a To-do item"""
    try:
        todo = (
            db.query(Todo)
            .filter(Todo.id == todo_id, Todo.owner_id == current_user.id)
            .first()
        )
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        return_todo = [ReturnTodo(**todo.__dict__)]
        return return_todo
    except HTTPException as http_exc:
        # Re-raise the HTTPException to ensure FastAPI handles it
        raise http_exc
    except Exception as err:
        error_message = f"Internal Server Error: {err}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@router.delete("/todos/{todo_id}", response_model=None)
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(verify_token),
    db: Session = Depends(get_db),
):
    """Delete a todo item by ID"""
    try:
        # Query the database to find the todo item
        todo = (
            db.query(Todo)
            .filter(Todo.id == todo_id, Todo.owner_id == current_user.id)
            .first()
        )

        if not todo:
            # If the todo item is not found, raise a 404 Not Found exception
            raise HTTPException(status_code=404, detail="Todo not found")

        # Delete the todo item from the database
        db.delete(todo)
        db.commit()

        # Return a success response
        return {"message": f"Todo with ID {todo_id} has been removed"}
    except HTTPException as http_exc:
        # Re-raise the HTTPException to ensure FastAPI handles it
        raise http_exc

    except Exception as err:
        # Handle any other exceptions and return a 500 Internal Server Error
        error_message = f"Internal Server Error: {err}"
        logging.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)
