""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from pydantic import BaseModel
import json

with open("../secrets/secrets.json", "r") as config_file:
    config = json.load(config_file)


# SQLAlchemy models
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Establish a one-to-many relationship with Todo
    todos = relationship("Todo", back_populates="owner")

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Boolean, default=False)

    # Establish a many-to-one relationship with User
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")


# Create the database engine
db_url = (
    f"postgresql://{config['postgres']['db_user']}:{config['postgres']['db_password']}"
    f"@{config['postgres']['db_host']}:{config['postgres']['db_port']}/{config['postgres']['db_name']}"
)

# db_url = "postgresql://postgres:D@rkpostgresgr33n@localhost:5432/mytest"

engine = create_engine(db_url)

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
