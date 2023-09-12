""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    text,
    MetaData,
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv

# Get the directory containing your script (data folder)
script_directory = os.path.dirname(__file__)

# Construct the path to the secrets.env file relative to your script's location
dotenv_path = os.path.join(script_directory, "..", "secrets", "secrets.env")
load_dotenv(dotenv_path)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


# SQLAlchemy models
Base = declarative_base()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Create the database engine
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

# Specify a scheme name
schema_name = "new_schema"
create_schema_sql = text(f"CREATE SCHEMA {schema_name};")

# Execute the SQL query to create the schema
with engine.connect() as connection:
    connection.execute(create_schema_sql)


class User(Base):
    __tablename__ = f"{schema_name}.users"
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
    __tablename__ = f"{schema_name}.todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(Boolean, default=False)

    # Establish a many-to-one relationship with User
    owner_id = Column(Integer, ForeignKey(f"{schema_name}.users.id"))
    owner = relationship("User", back_populates=f"{schema_name}.todos")


# Create a MetaData object
metadata = MetaData(schema=schema_name)

# Create tables
Base.metadata.clear()
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
