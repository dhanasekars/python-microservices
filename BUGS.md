# Bugs

1. :white_check_mark:  Hardcoded path in todo.json file path -helper.py 
2. :white_check_mark: PUT endpoint needs all three fields, fix the Pydantic BaseModel with non-mandatory fields
3. :white_check_mark: PUT - Handle updating an existing todo item with empty body {} 
4. :white_check_mark: a todo_helper test `test_save_list_json_decode_error` is disabled as it's corrupting the json, that makes integration tests fail.
        RCA - missed to patch mock_open, fixed code
  
      ```python
          @patch("builtins.open", mock_open()) # This patch was missed
          @patch("json.dump", side_effect=json.JSONDecodeError("Test error", "", 0))
          def test_save_list_json_decode_error(self, mock_open):
              # Arrange
              todo_list = ["Task 1", "Task 2"]
      
              # Act
              result = save_list(todo_list)
      
              # Assert
              self.assertEqual(result, "Error encoding data to JSON.") 
      ```
 
- [ ] A test is creating the json.data - fix that. This happens when there is no json file 
