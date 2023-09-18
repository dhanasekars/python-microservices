""" 
Created on : 18/08/23 8:37 am
@author : ds  
"""
from fastapi import FastAPI
from app.apis import todos
from app.data.setup import connect_to_database, create_tables


app = FastAPI()


def config_app():
    """To include router from other modules"""
    app.include_router(todos.router)


def config_database():
    engine = connect_to_database()
    create_tables(engine)
    engine.dispose()


config_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
