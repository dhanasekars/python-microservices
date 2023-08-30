""" 
Created on : 30/08/23 3:33 pm
@author : ds  
"""

import json
import os


class ConfigurationManager:
    config_data: object
    _instance = None  # Private class variable to store the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(script_dir, "config.json")

        try:
            with open(config_file_path, "r") as config_file:
                self.config_data = json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in config file.")
        except Exception as e:
            raise Exception(f"Error loading config file: {str(e)}")


# Create an instance of the ConfigurationManager
config_manager = ConfigurationManager()
