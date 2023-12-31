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

cc:
	#clearing all pytest cache
	find . -type f -name ".coverage.DSs-MacBook-Pro.local*" -exec rm -f {} \;
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type f -name ".coverage" -exec rm -r {} +


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


startpg:
	brew services start postgresql@15

stoppg:
	brew services stop postgresql@15

restartpg:
	brew services restart postgresql@15

dcbuild:
	docker-compose build
dcup:
	docker-compose --env-file app/secrets/.env.docker up

dcdown:
	docker-compose down

unittests:
	cd app && poetry run python -m pytest --cov  --cov-report=term-missing tests/01_unit_tests

integrationtests:
	cd app && poetry run python -m pytest --cov --cov-report=term-missing tests/02_integration_tests

test: unittests integrationtests cc

routine: cc deletelog test git cc

all: routine dcbuild dcup