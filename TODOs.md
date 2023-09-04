# Todos
## September 
- [x] Patch entire class check unittest for get_todo_list()
  - use @patch decorator before class declaration to patch a function for all tests inside the class
- [x] Unit tests for all function.
- [x] Add debug logging to the project
- [x] Create a config.json file
- [x] Return appropriate HTTP status codes 
- [ ] Integration / functional tests
- [ ] Make Production ready
  - [ ] Restructure project
  - [ ] Containerization  
  - [ ] Establish CI/CD
  - [ ] Host it in cloud

## Later
- [ ] Head, Options, Patch and Trace
- [ ] Move data store from json to db
- [ ] Authentication 
- [ ] tracking and limiting usage 
- [ ] Have an error message json
- [ ] Generate total time spent for this project from README.md


# Bugs

- [x] Hardcoded path in todo.json file path -helper.py 
- [x] PUT endpoint needs all three fields, fix the Pydantic BaseModel with non-mandatory fields
- [x] PUT - Handle updating an existing todo item with empty body {} 
- [ ] A test is creating the json.data - fix that. This happens when there is no json file 