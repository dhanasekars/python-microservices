install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install
format:
	#format code
	black *.py source/*.py
lint:
	#flake8 or #pylint
	pylint *.py source/*.py
test:
	#test
	python -m pytest -vv --cov=source --cov=main test_*.py

deploy:
	#deploy
all: install format lint test deploy