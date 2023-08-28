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
routine: test git
all: install format lint test