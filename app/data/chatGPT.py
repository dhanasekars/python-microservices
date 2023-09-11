""" 
Created on : 10/09/23 3:42 pm
@author : ds  
"""
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Define the SQLAlchemy models
Base = declarative_base()


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
db_url = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
engine = create_engine(db_url)

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


# Define the Pydantic model for user registration
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str


# Define JWT settings
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create a FastAPI app
app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to create an access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Registration endpoint with JWT token generation
@app.post("/register/", response_model=User)
def register_user(user_data: UserCreate, db: Session = Depends(session)):
    # Check if a user with the same username or email already exists
    existing_user = (
        db.query(User)
        .filter(User.username == user_data.username or User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this username or email already exists"
        )

    # Hash the password and create the new user
    new_user = User(**user_data.dict(exclude={"password"}))
    new_user.set_password(user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate a JWT token upon successful registration
    access_token = create_access_token(data={"sub": new_user.username})
    return {"user": new_user, "access_token": access_token}


# Token Pydantic model
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
