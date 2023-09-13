""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""

from fastapi import HTTPException
import logging
from passlib.context import CryptContext
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.exc import SQLAlchemyError
import psycopg2
from psycopg2 import errors
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    MetaData,
)
from sqlalchemy.orm import relationship, declarative_base
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.utils.config_manager import config_manager

# Configure JWT settings (you can use your own secret key)
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

config_manager.configure_logging()
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
db_schema = os.getenv("DB_SCHEMA", "public")


# Create the database engine
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def connect_to_database():
    """Connect to the database and create it if it doesn't exist."""
    try:
        # Connect to the PostgreSQL server
        engine = create_engine(db_url)

        # Check if the database already exists
        if not database_exists(engine.url):
            # If it doesn't exist, create the new database
            create_database(engine.url)
            print(f"Database '{db_name}' created successfully.")
            logging.info(f"Database '{db_name}' created successfully.")

        else:
            print(f"Database '{db_name}' already exists.")
            logging.info(f"Database '{db_name}' already exists.")

        return engine

    except SQLAlchemyError as sae:
        if isinstance(sae.orig, errors.DuplicateDatabase):
            logging.info(f"Database '{db_name}' already exists.")
        else:
            logging.error(f"SQLAlchemy Error: {sae}")
            raise HTTPException(status_code=500, detail="Database connection error")
    except psycopg2.Error as pe:
        logging.error(f"Psycopg2 Error: {pe}")
        raise HTTPException(status_code=500, detail="Database connection error")


def create_tables(engine):
    """Create tables in the database."""
    try:
        Base = declarative_base(metadata=MetaData())

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

        Base.metadata.create_all(engine)
        print("Tables created successfully.")
        logging.info("Tables created successfully.")

    except SQLAlchemyError as sae:
        logging.error(f"SQLAlchemy Error: {sae}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except psycopg2.Error as pe:
        logging.error(f"Psycopg2 Error: {pe}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

    return User, Todo


# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
