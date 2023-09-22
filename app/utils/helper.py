""" 
Created on : 26/08/23 11:27 am
@author : ds  
"""
import uuid
import logging
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.data import models
from app.data.models import User, Todo, RegistrationRequest
from app.utils.config_manager import config_manager

config_manager.configure_logging()


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_new_user(db: Session, user_data: RegistrationRequest):
    """function to register a new user"""
    hashed_password = pwd_context.hash(user_data.password)

    db_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def load_user_todos(current_user: User, page: int, per_page: int, db: Session):
    """Load to-do items for the authenticated user from the database."""
    try:
        # Calculate the offset for pagination
        skip = (page - 1) * per_page

        # Query the database to retrieve the to-do items for the current user
        todos = (
            db.query(Todo)
            .filter(Todo.owner_id == current_user.id)
            .offset(skip)
            .limit(per_page)
            .all()
        )

        return todos
    except Exception as err:
        logging.error(f"Error loading user's to-do list: {str(err)}")
        raise HTTPException(
            status_code=500, detail=f"Error loading user's to-do list: {str(err)}"
        )


def generate_id():
    """generate a UUID for each task"""
    new_id = uuid.uuid4().hex
    logging.debug(f"Generated new ID: {new_id}")
    return new_id
