MSG ?= Daily practise

install:
	#install commands
	curl -sSL https://install.python-poetry.org | python3 - &&\
 		  poetry self update &&\
 		  poetry install

format:
	#format code
	black app/../

lint:
	#flake8 or #pylint
	pylint -j 4 --rcfile=pylint.rc app/

git:
	#git push
	git add .
	git commit -m "$(MSG)"
	git push origin working-tree

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

check: format lint

listvenv:
	find / -type d -name 'bin' -exec sh -c 'if [ -f "{}/activate" ]; then dirname "{}"; fi' \;

docker_build:
	docker pull dhanasekars/my-todos:latest
	docker run -p 80:8000 my-todos

startpg:
	brew services start postgresql@15

stoppg:
	brew services stop postgresql@15

restartpg:
	brew services restart postgresql@15

dcup:
	docker-compose --env-file app/secrets/.env.docker up

dcdown:
	docker-compose down

unittests:
	cd app && poetry run python -m pytest --cov  --cov-report=term-missing tests/01_unit_tests

integrationtests:
	cd app && poetry run python -m pytest --cov --cov-report=term-missing tests/02_integration_tests

test: unittests integrationtests

routine: clean_cache test git clean_cache

all: routine dcup