## Todos
- [x] Patch entire class check unittest for get_todo_list()
  - use @patch decorator before class declaration to patch a function for all tests inside the class
- [ ] Unit tests for all function.
- [ ] Add debug logging to the project
- [x] Create a config.json file
- [ ] Head, Options, Patch and Trace
- [ ] Host it in cloud
- [ ] Storage to db from flat json file
- [ ] Authentication 
- [ ] tracking and limiting usage 
- [ ] Have an error message json

## Bugs

- [x] Hardcoded path in todo.json file path -helper.py 
- [x] PUT endpoint needs all three fields, fix the Pydantic BaseModel with non-mandatory fields
- [ ] PUT - Handle updating an existing todo item with empty body {} 