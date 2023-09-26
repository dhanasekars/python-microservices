""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""
import os
import logging

from fastapi import HTTPException
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.models import Base
from utils.config_manager import config_manager


config_manager.configure_logging()
# Get the directory containing your script (data folder)
config_manager.get_secrets()

db_user = os.getenv("TODOLIST_ADMIN")
db_password = os.getenv("TODO_ADMIN_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("TODOLIST_DB")
db_schema = os.getenv("POSTGRES_SCHEMA", "public")


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
