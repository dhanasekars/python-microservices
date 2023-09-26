""" 
Created on : 30/08/23 3:33 pm
@author : ds  
"""

import json
import os
import logging

from dotenv import load_dotenv


class ConfigurationManager:
    """Singleton class to load and store the configuration data."""

    config_data: object
    _instance = None  # Private class variable to store the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigurationManager, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        """Get the directory of the current script"""

        if "GITHUB_ACTIONS" in os.environ:
            # Running in GitHub Actions
            github_workspace = os.environ.get("GITHUB_WORKSPACE")
            if not github_workspace:
                raise EnvironmentError(
                    "GITHUB_WORKSPACE environment variable not found."
                )

            config_file_relative_path = (
                "app/config/config.json"  # Relative to the root of your repository
            )
            config_file_path = os.path.join(github_workspace, config_file_relative_path)
        else:
            # Running locally
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_file_relative_path = "../config/config.json"
            config_file_path = os.path.abspath(
                os.path.join(script_dir, config_file_relative_path)
            )
        try:
            with open(config_file_path, "r", encoding="UTF8") as config_file:
                self.config_data = json.load(config_file)
        except FileNotFoundError:
            raise FileNotFoundError("Config file not found.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in config file.")
        except Exception as err:
            raise Exception(f"Error loading config file: {str(err)}")

    def configure_logging(self):
        """Configure logging using the loaded configuration"""
        log_level_str = self.config_data["logging_config"]["level"].upper()
        log_level = getattr(logging, log_level_str)
        log_format = self.config_data["logging_config"]["format"]
        log_file = self.config_data["logging_config"]["filename"]
        log_file_mode = self.config_data["logging_config"]["filemode"]

        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format=log_format,
            filemode=log_file_mode,
        )
        logging.getLogger()

    def get_secrets(self):
        """Load the secrets from the environment-specific .env file"""
        environment = os.environ.get("MY_ENVIRONMENT")
        if environment == "local":
            dotenv_file = ".env.local"
        elif environment == "docker" or "GITHUB_ACTIONS" in os.environ:
            dotenv_file = ".env.docker"
        else:
            raise ValueError(
                "Invalid or unspecified environment. Set MY_ENVIRONMENT to 'local' or 'docker'."
            )

        script_directory = os.path.dirname(__file__)
        # Construct the path to the environment-specific .env file
        dotenv_path = os.path.join(script_directory, "..", "secrets", dotenv_file)
        load_dotenv(dotenv_path)


# Create an instance of the ConfigurationManager
config_manager = ConfigurationManager()
