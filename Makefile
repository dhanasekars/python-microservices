MSG ?= Daily practise

install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install

format:
	#format code
	black *.py app/../*.py

lint:
	#flake8 or #pylint
	pylint *.py app/../*.py

test:
	#test
	python -m pytest -vv --cov=app/apis --cov=app/utils
	coverage report --show-missing

git:
	#git push
	git add .
	git commit -m "$(MSG)"
	git push

start:
	uvicorn main:app --reload

clean_cache:
	#clearing all pytest cache
	find . -type d -name ".pytest_cache" -exec rm -r {} +

coverage_for_function:
	# This is to check coverage for a given function using pytest
	pytest --cov=my_module -k my_function

deletelog:
	# Delete the log file
	/bin/rm -f app/log/*

source:
	source ~/.zshrc

routine: deletelog clean_cache test clean_cache git

check: format lint

listvenv:
	find / -type d -name 'bin' -exec sh -c 'if [ -f "{}/activate" ]; then dirname "{}"; fi' \;
