""" 
Created on : 18/09/23 4:53 pm
@author : ds  
"""
import os
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.data.models import TokenData, User
from app.data.setup import get_db
from app.utils.config_manager import config_manager

config_manager.get_secrets()
# Configure JWT settings
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# Create an instance of the token security class
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create a password context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to generate an access token
def create_access_token(data: dict, expires_delta: timedelta):
    """Create an access token with the given data and expiration date."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify the password
# def verify_password(plain_password, hashed_password):
#     """Verify the password against the hashed password."""
#     return pwd_context.verify(plain_password, hashed_password)


# def get_user(db, username: str):
#     """Get a user from the database."""
#     return db, username
#
#
# def authenticate_user(db, username: str, password: str):
#     """Authenticate a user and return user details."""
#     user = get_user(db, username)
#     if not user:
#         return None
#     if not verify_password(password, user.password):
#         return None
#     return user


def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get the current user from the access token."""
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("username is None. Input blank")
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            print("user is None. No user found with that username in db")
            raise credentials_exception
    except JWTError:
        print("JWTError")
        raise credentials_exception
    return user
