""" 
Created on : 30/08/23 11:34 am
@author : ds  
"""
import json
import unittest
from unittest.mock import mock_open, patch
from utils.todo_helper import save_list, load_list, get_todo_details


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

    # Test case: JSONDecodeError raised for a non-JSON format
    @patch(
        "json.loads",
        side_effect=json.JSONDecodeError("Expecting value.", "Test.", 0),
    )
    def test_json_decode_error(self, mock_json_loads):
        self.assertEqual(load_list().msg, "Expecting value.")
        self.assertEqual(load_list().doc, "Test.")


@patch("utils.todo_helper.load_list", autospec=True)
class TestGetTodoDetails(unittest.TestCase):
    """create test class that inherits from unitest.Testcase to test Get Todo Details helper function"""

    def test_valid_todo_id(self, mock_load_list):
        mock_data = [{"id": 1, "task": "Task 1", "status": "Incomplete"}]
        mock_load_list.return_value = mock_data
        expected_result = {"id": 1, "task": "Task 1", "status": "Incomplete"}
        self.assertEqual(get_todo_details(1), expected_result)

    def test_invalid_todo_id(self, mock_load_list):
        mock_data = [{"id": 1, "task": "Task 1", "status": "Incomplete"}]
        mock_load_list.return_value = mock_data
        result = get_todo_details(2)
        self.assertIsInstance(result, dict)
        assert "error" in result
        self.assertEqual(result["error"], "Todo not found for the given id.")

    def test_invalid_data_format(self, mock_load_list):
        mock_data = "invalid json"
        mock_load_list.return_value = mock_data
        result = get_todo_details(2)
        self.assertIsInstance(result, dict)
        assert "error" in result
        self.assertEqual(result["error"], "Invalid data format. Expected a list.")

    def test_empty_data(self, mock_load_list):
        mock_data = []
        mock_load_list.return_value = mock_data
        result = get_todo_details(2)
        self.assertIsInstance(result, dict)
        assert "error" in result
        self.assertEqual(result["error"], "No data in the system.")
