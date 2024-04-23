# Makefile

# Set the directory of your Python code through an environment variable, default to the current directory
CODE_DIR ?= .

# The application to run with uvicorn
APP_MODULE ?= main:app

# Command to format the code with black
format:
	black $(CODE_DIR)

# Command to sort imports with isort
sort:
	isort $(CODE_DIR)

# Command to lint the code with pylint
lint:
	pylint $(CODE_DIR)

# Command to run the application using uvicorn with the --reload flag
run:
	uvicorn $(APP_MODULE) --reload

# Migration message variable
MIGRATION_MSG ?= "Initial migration"

# Command to generate a new Alembic migration
migrate-create:
	alembic revision --autogenerate -m $(MIGRATION_MSG)

# Command to run migrations to the latest version
migrate-up:
	alembic upgrade head

# Command to count the number of files tracked by Git
count-files:
	@echo "Counting files tracked by Git..."
	@echo $(shell git ls-files | wc -l) files are tracked by Git.

# Command to run all of the formatting and linting
all: sort format lint

.PHONY: format sort lint run migrate-create migrate-up count-files all