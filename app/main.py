""" 
Created on : 18/08/23 8:37 am
@author : ds  
"""
from fastapi import FastAPI
from app.apis import todos

app = FastAPI()


def configuration():
    """To include router from other modules"""
    app.include_router(todos.router)


configuration()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
