""" 
Created on : 26/08/23 6:15 pm
@author : ds  
"""

# import logging
# from config.config_manager import config_manager
# from pydantic import BaseModel, Field, constr, model_validator, ValidationError
# from typing import Optional, List

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

# config_manager.load_config()
#
# print(config_manager.config_data["logging_config"])
#
# logging.debug("This is test message.")
# logging.info("This is info message")


from pydantic import (
    BaseModel,
    field_validator,
    constr,
    conint,
    ValidationError,
    model_validator,
)
from typing import Optional


class UpdateTodo(BaseModel):
    """Model with optional fields where at least one must have a value."""

    title: Optional[constr(min_length=1)] = None
    description: Optional[str] = None
    doneStatus: Optional[bool] = None

    @model_validator(mode="before")
    def check_blank_fields(cls, values):
        print(values)
        num_fields_with_values = sum(
            1 for value in values.values() if value is not None
        )
        if num_fields_with_values < 1:
            raise ValueError(
                "At least one of 'title', 'description', or 'doneStatus' must have a value"
            )
        return values


try:
    output = UpdateTodo(description="", doneStatus=True)
except ValidationError as e:
    print(e)


# import re
#
# uuid_hex_regex = re.compile(
#     r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
# )
#
# # Test the regex with a UUID
# uuid_string = "0ef3a021e5544c18bdf2c71a3b1e3884"
# if uuid_hex_regex.match(uuid_string):
#     print("Valid UUID format")
# else:
#     print("Invalid UUID format")


