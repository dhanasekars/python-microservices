""" 
Created on : 30/08/23 11:34 am
@author : ds  
"""
import json
import unittest
from unittest.mock import mock_open, patch
from fastapi import HTTPException

import pytest

from app.utils.helper import (
    save_list,
    load_list,
    get_todo_details,
    remove_todo,
    generate_id,
    update_todo,
)
from app.utils.config_manager import config_manager


# ------------------------test setup ----------------------------------#
# Mock functions for load_list and save_list
def mock_load_list():
    return [{"id": 1, "task": "Task 1"}, {"id": 2, "task": "Task 2"}]


def mock_save_list(data):
    mock_save_list.updated_data = data


class TestLoadListFromJSON(unittest.TestCase):
    # Test case - Loading a list from a valid JSON file
    @patch("builtins.open", new_callable=mock_open, read_data="[1, 2, 3, 4, 5]")
    def test_load_list_from_json_valid(self, mock_file_open):
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
    @patch("builtins.open", new_callable=mock_open, read_data="[1, 2, 3, 4, 5]")
    def test_json_decode_error(self, mock_file_open, mock_json_loads):
        self.assertEqual(load_list().msg, "Expecting value.")
        self.assertEqual(load_list().doc, "Test.")


@patch("app.utils.helper.load_list")
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
        with pytest.raises(HTTPException) as execinfo:
            remove_todo(2)
        self.assertEqual(execinfo.value.status_code, 404)
        self.assertEqual(execinfo.value.detail, "ID not found")

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


class TestSaveList(unittest.TestCase):
    """create test class that inherits from unitest.Testcase to test Get save list helper function"""

    @patch("builtins.open", new_callable=mock_open)
    def test_save_list_success(self, mock_file):
        todo_list = [
            {
                "title": "This is the second task.",
                "description": "",
                "doneStatus": False,
                "id": "062a2f32f2d54a5c94cd64c4013ee58b",
            }
        ]
        result = save_list(todo_list=todo_list)
        self.assertTrue(result)
        mock_file.assert_called_once_with(
            config_manager.config_data.get("data_file"), "w", encoding="utf-8"
        )
        mock_file().write.assert_called()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_save_list_file_not_found(self, mock_file):
        # Arrange
        todo_list = ["Task 1", "Task 2"]

        # Act
        result = save_list(todo_list)

        # Assert
        self.assertEqual(result, "File not found. Check the file path.")

    @patch("builtins.open", side_effect=PermissionError)
    def test_save_list_permission_error(self, mock_open):
        # Arrange
        todo_list = ["Task 1", "Task 2"]

        # Act
        result = save_list(todo_list)

        # Assert
        self.assertEqual(result, "Permission denied. Check file permissions.")

    @patch("builtins.open", side_effect=Exception("Test exception"))
    def test_save_list_generic_exception(self, mock_open):
        # Arrange
        todo_list = ["Task 1", "Task 2"]

        # Act
        result = save_list(todo_list)

        # Assert
        self.assertEqual(result, "An unexpected error occurred: Test exception")

    @patch("builtins.open", mock_open())
    @patch("json.dump", side_effect=json.JSONDecodeError("Test error", "", 0))
    def test_save_list_json_decode_error(self, mock_open):
        # Arrange
        todo_list = ["Task 1", "Task 2"]

        # Act
        result = save_list(todo_list)

        # Assert
        self.assertEqual(result, "Error encoding data to JSON.")


@patch("app.utils.helper.load_list", side_effect=mock_load_list)
@patch("app.utils.helper.save_list", side_effect=mock_save_list)
class TestRemoveTodo(unittest.TestCase):
    """module to test Remove todo item"""

    def test_remove_existing_todo(self, mock_load, mock_save):
        with pytest.raises(HTTPException) as execinfo:
            remove_todo(1)
        self.assertEqual(execinfo.value.status_code, 200)
        self.assertEqual(execinfo.value.detail, "Item with ID 1 removed")

    def test_remove_nonexistent_todo(self, mock_load, mock_save):
        with pytest.raises(HTTPException) as execinfo:
            remove_todo(3)
        self.assertEqual(execinfo.value.status_code, 404)
        self.assertEqual(execinfo.value.detail, "ID not found")

    def test_remove_last_todo(self, mock_load, mock_save):
        with pytest.raises(HTTPException) as execinfo:
            remove_todo(2)
        self.assertEqual(execinfo.value.status_code, 200)
        self.assertEqual(execinfo.value.detail, "Item with ID 2 removed")


class TestGenerateID(unittest.TestCase):
    """module to test UUID generation and uniqueness"""

    def test_generate_id_length(self):
        # Generate an ID and check if it has the correct length
        generated_id = generate_id()
        self.assertEqual(len(generated_id), 32)  # A UUID4 hex string has 32 characters

    def test_generate_id_uniqueness(self):
        # Generate a list of IDs and ensure they are all unique
        id_list = [generate_id() for _ in range(100)]
        self.assertEqual(len(id_list), len(set(id_list)))  # Check for uniqueness


@patch("app.utils.helper.load_list", side_effect=mock_load_list)
@patch("app.utils.helper.save_list", side_effect=mock_save_list)
class TestUpdateTodo(unittest.TestCase):
    def test_update_existing_todo(self, mock_save, mock_load):
        # Update an existing todo
        result = update_todo(1, {"task": "Updated Task"})
        self.assertEqual(result, {"success": "1 updated successfully."})

        # Verify that the todo was actually updated
        self.assertEqual(
            mock_save.call_args[0][0],
            [{"id": 1, "task": "Updated Task"}, {"id": 2, "task": "Task 2"}],
        )

    def test_update_nonexistent_todo(self, mock_save, mock_load):
        # Try to update a nonexistent todo
        with pytest.raises(HTTPException) as execinfo:
            update_todo(5, {"task": "Updated Task"})
        self.assertEqual(execinfo.value.status_code, 404)
        self.assertEqual(execinfo.value.detail, "5 not found.")
        self.assertIsNone(mock_save.call_args)

    def test_update_with_invalid_key(self, mock_save, mock_load):
        # Try to update with an invalid key
        result = update_todo(1, {"invalid_key": "Updated Task"})
        self.assertEqual(result, {"success": "1 updated successfully."})

        # Verify that the todo list remains unchanged
        self.assertEqual(
            mock_save.call_args[0][0],
            [{"id": 1, "task": "Task 1"}, {"id": 2, "task": "Task 2"}],
        )
