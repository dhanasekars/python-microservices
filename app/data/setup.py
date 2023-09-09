""" 
Created on : 09/09/23 6:02 pm
@author : ds  
"""

import os

from app.utils.config_manager import config_manager

data = config_manager.config_data
print(type(data))
print(data)


data["username"] = os.environ.get("DATABASE_USERNAME", data["username"])
