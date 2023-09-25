""" 
Created on : 18/08/23 8:37 am
@author : ds  
"""
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from app.apis import todos
from app.data.setup import connect_to_database, create_tables

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def config_app():
    """To include router from other modules"""
    app.include_router(todos.router)


def config_database():
    """To create database and tables"""
    engine = connect_to_database()
    create_tables(engine)
    engine.dispose()


config_app()
config_database()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
