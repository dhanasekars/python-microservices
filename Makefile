install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install
format:
	#format code
lint:
	#flake8 or #pylint
test:
	#test
deploy:
	#deploy
all: install format lint test deploy