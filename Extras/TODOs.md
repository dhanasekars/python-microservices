## September

- [x] Patch entire class check unittest for get_todo_list()
  - use @patch decorator before class declaration to patch a function for all tests inside the class
- [x] Unit tests for all function.
- [x] Add debug logging to the project
- [x] Create a config.json file
- [x] Return appropriate HTTP status codes 
- [X] Integration / functional tests
- [x] Restructure project
- [x] Containerization  
- [x] Establish CI/CD in - Git Actions
- [ ] Move data store from json to db
  - [x] Create a db connection
  - [x] Create a db tables
  - [x] Create a db connection pool
  - [x] test_todo.py tests fail if the db server is not running, fix it
  - [x] Integration test for registration
  - [ ] Update all functions to use db connection
  - [ ] Set up a Docker container for db server
  - [ ] Make integration tests to run in Git actions by creating a db server in Git actions
- [x] - Run unit tests in parallel, measure current execution time before moving to parallel execution. 
        used pytest-xdist plugin - 57 tests took 3.73s and with 3 workers it took 2.88s. 
        But for now in pipeline no parallel execution.
- [ ] Authentication
- [ ] Update the test fixture @generateUDID 
- [ ] Tracking and limiting usage 
- [ ] Have an error message json
- [ ] Host it in cloud
- [ ] Add release notes
- [ ] Maintain release version numbers
- 
## Later

- [ ] Connect to more than one type of DB and test ( Postgres, MySQL, SQLite)
- [ ] Head, Options, Patch and Trace
- [ ] Generate total time spent for this project from README.md
- [ ] Fix all lint issues
- [ ] Explore Fire
- [ ] Confirm schema for db by passing the schema name in secrets.env
- [ ] Create admin API - to activate, de-active, delete users. 
- [ ] Annotate dependencies using SQLAlchemy type annotations or is it pydantic?
- [ ] Reqover coverage
- [ ] Explore query builder 

### Action items
 - [ ] is it necessary to install libpq separately using brew? 