""" 
Created on : 30/08/23 11:34 am
@author : ds  
"""
import unittest
from unittest.mock import mock_open, patch
from utils.helper import save_list, load_list


class TestLoadListFromJSON(unittest.TestCase):
    # Test case - Loading a list from a valid JSON file
    @patch("builtins.open", new_callable=mock_open, read_data="[1, 2, 3, 4, 5]")
    def test_load_list_from_json_valid(self, mock_file_open):
        loaded_list = load_list()
        self.assertEqual(load_list(), [1, 2, 3, 4, 5])

    # Test case: Return an empty list from a non-existent file
    @patch("builtins.open", side_effect=FileNotFoundError("file not found"))
    def test_load_list_from_json_nonexistent_file(self, mock_file_open):
        self.assertEqual(load_list(), [])
