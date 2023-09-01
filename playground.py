""" 
Created on : 26/08/23 6:15 pm
@author : ds  
"""
# import uuid
#
#
# def generate_id():
#     return uuid.uuid1().hex
#
#
# print(generate_id())


# from typing import Optional
#
# from pydantic import BaseModel, ValidationError
#
#
# class Foo(BaseModel):
#     f1: str  # required, cannot be None
#     f2: Optional[str]  # required, can be None - same as str | None
#     f3: Optional[str] = None  # not required, can be None
#     f4: str = "Foobar"  # not required, but cannot be None
#
#
# try:
#     output = Foo(f1="test", f2=None, f4="hello")
# except ValidationError as e:
#     print(e)
