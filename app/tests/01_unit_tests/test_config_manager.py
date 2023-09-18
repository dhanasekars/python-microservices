""" 
Created on : 18/09/23 10:34 am
@author : ds  
"""
import json
import unittest
from unittest.mock import patch, mock_open
from app.utils.config_manager import ConfigurationManager


class TestConfigLoader(unittest.TestCase):
    """class to test the configuration loader"""

    def test_load_config(self):
        """Test that the configuration data is loaded correctly"""
        with unittest.mock.patch("builtins.open") as mock_open_file:
            # Mock the return value of the open function
            mock_open_file.return_value.__enter__.return_value.read.return_value = (
                '{"key": "value"}'
            )

            # Create an instance of your configuration class
            config_loader = ConfigurationManager()

            # Call the load_config method
            config_loader.load_config()

            # Assert that the configuration data is loaded correctly
            self.assertEqual(config_loader.config_data, {"key": "value"})

    @patch("builtins.open")
    def test_file_not_found_exception(self, mock_open_file):
        """Test that a FileNotFoundError is raised if the config file is not found."""

        # Mock open function to raise FileNotFoundError
        mock_open_file.side_effect = FileNotFoundError

        # Create an instance of your configuration class
        config_loader = ConfigurationManager()

        # Assert that the FileNotFoundError is raised with the expected message
        with self.assertRaises(FileNotFoundError) as context:
            config_loader.load_config()
        self.assertEqual(str(context.exception), "Config file not found.")

    @patch("builtins.open")
    def test_generic_exception(self, mock_open_file):
        """Test that a generic Exception is raised if the config file cannot be loaded."""

        # Mock open function to raise a generic Exception
        mock_open_file.side_effect = Exception("Some error")

        # Create an instance of your configuration class
        config_loader = ConfigurationManager()

        # Assert that a generic Exception is raised with the expected message
        with self.assertRaises(Exception) as context:
            config_loader.load_config()
        self.assertEqual(
            str(context.exception), "Error loading config file: Some error"
        )

    @patch(
        "json.loads",
        side_effect=json.JSONDecodeError("Expecting value.", "Test.", 0),
    )
    @patch("builtins.open", new_callable=mock_open, read_data="[1, 2, 3, 4, 5]")
    def test_json_decode_error_exception(self, _, __):
        """Test that a JSONDecodeError is raised if the config file contains invalid JSON."""

        # Create an instance of your configuration class
        mock_open.side_effect = Exception("Some error")

        config_loader = ConfigurationManager()

        # Assert that a JSONDecodeError is raised with the expected message
        with self.assertRaises(ValueError) as context:
            config_loader.load_config()
        self.assertEqual(str(context.exception), "Invalid JSON format in config file.")

    @patch.dict(
        "os.environ",
        {"GITHUB_ACTIONS": "true", "GITHUB_WORKSPACE": "/path/to/github/workspace"},
    )
    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_github_actions(self, _):
        """Test that the configuration data is loaded correctly when running in GitHub Actions."""

        # Create an instance of your configuration class
        config_loader = ConfigurationManager()

        # Call the load_config method
        config_loader.load_config()

        # Assert that the configuration data is loaded correctly
        self.assertEqual(config_loader.config_data, {"key": "value"})

    @patch.dict(
        "os.environ",
        {"GITHUB_ACTIONS": "true", "GITHUB_WORKSPACE": ""},
    )
    def test_github_actions_environment_exception(self):
        """Test that an EnvironmentError is raised
        if the GITHUB_WORKSPACE environment variable is not set."""

        # Assert that the configuration data is loaded correctly
        with self.assertRaises(EnvironmentError) as context:
            config_loader = ConfigurationManager()
            config_loader.load_config()
        self.assertEqual(
            str(context.exception), "GITHUB_WORKSPACE environment variable not found."
        )
