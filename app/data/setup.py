""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import HTTPException
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import sessionmaker
from jose import jwt

from app.data.models import Base
from app.utils.config_manager import config_manager


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

# Configure JWT settings
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# Create the database engine
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)


def connect_to_database():
    """Connect to the database and create it if it doesn't exist."""
    try:
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

    except Exception as err:
        logging.error(f"Error: {err}")
        raise HTTPException(status_code=500, detail="Database connection error")


def create_tables(db_engine):
    """Create tables in the database."""

    try:
        Base.metadata.create_all(db_engine)
        print("Tables created successfully.")
        logging.info("Tables created successfully.")

    except Exception as err:
        logging.error(f"Error: {err}")
        raise HTTPException(status_code=500, detail="Database connection error")


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database connection."""
    db_session = SessionLocal()
    try:
        return db_session
    finally:
        db_session.close()


# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta):
    """Create an access token with the given data and expiration date."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
