

unittests:
	# Run all unittests
	poetry run python -m pytest --cov  --cov-report=term-missing tests/01_unit_tests

integrationtests:
	# Run all integration tests
	poetry run python -m pytest --cov --cov-report=term-missing tests/02_integration_tests

alltests: unittests integrationtests

start:
	uvicorn main:app --reload

hardstart:
	poetry run python main.py

startpg:
	brew services start postgresql@15

stoppg:
	brew services stop postgresql@15

restartpg:
	brew services restart postgresql@15

lint:
	#flake8 or #pylint
	pylint -j 4 --rcfile=pylint.rc app/