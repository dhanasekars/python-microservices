# Building microservices using FastAPI 

Create an API tutorial ( mimic ) https://www.eviltester.com/page/tools/apichallenges/ 
using Python and FastAPI 

## Other Learning Objectives

1. Pytest
2. Unit Test coverage
3. Poetry


### Spend one hour daily on this project

# Progress
<details>
    <summary>Day 1 : Aug 18  </summary>

`Time Spent : 50 minutes`

- Basic project structure
- Explored and implemented `Makefile`
- Basic understanding of `Poetry`
- Setup `sample_endpoint.py` and test file for it to configure pytest and test coverage

### References 
- https://www.youtube.com/watch?v=YB-_FsssK8E
- https://python-poetry.org/docs/basic-usage/
- https://www.gnu.org/software/make/manual/make.html

</details>




<details> 
    <summary> Day 2: Aug 19</summary>

`Time Spent : 50 minutes`


- :thumbsup: Set up route and todo route that returns  hardcoded value
- :thumbsdown: Unable to have the todo route as a separate module from main


</details>


<details> 
    <summary> Day 3: Aug 21</summary>

`Time Spent : 50 minutes`

- Pydantic
For GET request
- Async function 
- Pagination and per page

</details>

<details> 
    <summary> Day 4: Aug 22</summary>

`Time Spent : 50 minutes`

- Validation for page and per_page
- Unitest - statuscode done
- :thumbsdown: Unitest - content unable to do 
</details>

<details> 
    <summary> Day 5: Aug 24</summary>

- :thumbsup: Unitest Content done
- :thumbsup: Able to have the todo route as a separate module from main

Reference : https://www.youtube.com/watch?v=sBVb4IB3O_U

`Time Spent : 45 minutes`

</details>


<details> 
    <summary> Day 6: Aug 25</summary>

`Time Spent : 45 minutes`

:thumbsdown: tried to restructure data, reading from a json file and parsing.
Learned the problems of circular import, could not find the right solution but learnt why it is not working
Also, learn to rebase to last working version

This will undo any changes you've made to tracked files and restore deleted files:
```commandline
git reset HEAD --hard
```
This will delete any new files that were added since the last commit:
```commandline
git clean -fd
```
Files that are not tracked due to .gitignore are preserved; they will not be removed
Warning: using -x instead of -fd would delete ignored files. You probably don't want to do this.

Reference : [stack-overflow](https://stackoverflow.com/questions/4630312/reset-all-changes-after-last-commit-in-git)

</details>

<details> 
    <summary> Day 7: Aug 26</summary>

`Time Spent : 90 minutes`

- created helper file to read and save data to json file
- UUID generated 
- stuck with absolute path issue.
- Unit test is not working - need to use mock


_Added a step in Make file to test and push to git_

</details>

<details> 
    <summary> Day 8: Aug 27</summary>

`Time Spent : 45 minutes`

- Route to read an item using id
- Route to remove an item using id 

</details>

<details> 
    <summary> Day 9: Aug 28</summary>

- Route for update using PUT
- Learnt about limitation in FastAPI pydantic base model 
- This is the most complex so for. 

`Time Spent : 75 minutes`

</details>

<details> 
    <summary> Day 10: Aug 29</summary>

- No progress 
- Poetry env got screwed up while adding unit test (not sure about the root cause)
- Fixed the issue

Have to focus on unit tests tomorrow.

`Time Spent : 60 minutes`

</details>


-------------------------------
<details> 
    <summary> Day 0: Template</summary>

`Time Spent : XX minutes`

</details>