""" 
Created on : 20/09/23 9:43 am
@author : ds  
"""
from fastapi import HTTPException


class InvalidQueryParameter(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Invalid query parameters. Page and per_page must be positive integers.",
        )
