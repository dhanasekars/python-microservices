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
	pylint -j 4 --rcfile=pylint.rc app/

unittests:
	# Run all unittests
	poetry run python -m pytest --cov=app  --cov-report=term-missing app/tests/01_unit_tests

integrationtests:
	# Run all integration tests
	poetry run python -m pytest --cov=app --cov-report=term-missing app/tests/02_integration_tests


alltests: unittests integrationtests


git:
	#git push
	git add .
	git commit -m "$(MSG)"
	git push origin working-tree

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

routine: deletelog clean_cache restartpg alltests clean_cache git

check: format lint

listvenv:
	find / -type d -name 'bin' -exec sh -c 'if [ -f "{}/activate" ]; then dirname "{}"; fi' \;

docker_build:
	docker pull dhanasekars/my-todos:latest
	docker run -p 80:8000 my-todos

hardstart:
	poetry run python main.py

startpg:
	brew services start postgresql@15

stoppg:
	brew services stop postgresql@15

restartpg:
	brew services restart postgresql@15