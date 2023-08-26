install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install
format:
	#format code
	black *.py apis/*.py tests/*.py
lint:
	#flake8 or #pylint
	pylint *.py apis/*.py tests/*.py
test:
	#test
	python -m pytest -vv --cov=tests

git:
	#git push
	git add .
	git commit -m "daily practise"
	git push

routine: test git
all: install format lint test