install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install
format:
	#format code
	black *.py apis/*.py tests/*.py utils/*.py
lint:
	#flake8 or #pylint
	pylint *.py apis/*.py tests/*.py utils/*.py
test:
	#test
	python -m pytest -vv --cov=apis --cov=utils

git:
	#git push
	git add .
	git commit -m "daily practise"
	git push
start:
	uvicorn main:app --reload
clean_cache:
	#clearing all pytest cache
	find . -type d -name ".pytest_cache" -exec rm -r {} +


unittest:
	coverage run --rcfile=.coveragerc -m unittest tests/*.py
	coverage report -m


coverage_for_function:
	# This is to check coverage for a given function using pytest
	pytest --cov=my_module -k my_function


routine: clean_cache test unittest git

all: install format lint test

source:
	source ~/.zshrc
