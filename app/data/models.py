""" 
Created on : 18/09/23 5:28 am
@author : ds  
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, Field, model_validator
from pydantic import field_validator
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship, declarative_base
from passlib.context import CryptContext


Base = declarative_base(metadata=MetaData())
# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegistrationRequest(BaseModel):
    """Model for user registration"""

    username: constr(min_length=8, strip_whitespace=True)
    email: EmailStr
    password: constr(
        min_length=8, strip_whitespace=True
    )  # At least 1 uppercase letter and 1 digit

    @field_validator("password")
    def validate_password_format(cls, value):
        """function to validate password format"""
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        return value


class User(Base):
    """Base model for user"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Establish a one-to-many relationship with Todo
    todos = relationship("Todo", back_populates="owner")

    def set_password(self, password):
        """function to set password hash"""
        min_password_length = 8
        if password and len(password) >= min_password_length:
            self.password_hash = pwd_context.hash(password)
        else:
            self.password_hash = None

    def verify_password(self, password):
        """function to verify password hash"""
        return pwd_context.verify(password, self.password_hash)


class TodoItem(BaseModel):
    """Base model for to-do list"""

    title: constr(min_length=1, strip_whitespace=True)
    description: Optional[str] = None
    doneStatus: bool = Field(default=False)


class ReturnTodo(TodoItem):
    """extending TodoItem class with UUID"""

    id: str


class UpdateTodo(BaseModel):
    """Model with optional fields where at least one must have a value."""

    title: Optional[constr(min_length=1, strip_whitespace=True)] = None
    description: Optional[str] = None
    doneStatus: Optional[bool] = None

    @model_validator(mode="before")
    def check_blank_fields(cls, values):  # noqa: E0213
        """function to check at least one of the three fields is given"""
        num_fields_with_values = sum(
            1 for value in values.values() if value is not None
        )
        if num_fields_with_values < 1:
            raise ValueError(
                "At least one of 'title', 'description', or 'doneStatus' must have a value"
            )
        return values


class Todo(Base):
    """Base model for to-do list"""

    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Boolean, default=False)

    # Establish a many-to-one relationship with User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
