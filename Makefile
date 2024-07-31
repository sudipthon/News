# # Makefile

# # Set the default target
# .DEFAULT_GOAL := runserver

# # Define the virtual environment name
# VENV := venv

# # Install project dependencies
# install:
# 	poetry install

# # Create a virtual environment
# venv:
# 	poetry env use python3.9
# 	poetry install

# # Run Django development server
# runserver:
# 	poetry run python backend/manage.py runserver

# # Run Django migrations
# migrate:
# 	poetry run python backend/manage.py migrate

# # Create a new Django migration
# makemigrations:
# 	poetry run python manage.py makemigrations

# # Run Django tests
# test:
# 	poetry run python manage.py test

# # Clean up generated files
# clean:
# 	rm -rf $(VENV)
# 	find . -name "*.pyc" -delete


# target:
# 	recipie






#doing this lets makesystem know they aren't files but cmnds and speeds up the process,avoids conflicts if there are files with the same name
.PHONY: install rs mm mi ms csu shell t i-pre-commit u-pre-commit up-pre-commit


#installing pre-commit
i-pre-commit:
	poetry run pre-commit install

#uninstalling pre-commit
u-pre-commit:
	poetry run pre-commit uninstall

#updating pre-commit
up-pre-commit: u-pre-commit i-pre-commit


#installing dependencies
-i:
	poetry install

#runserver:
rs:
	poetry run python backend/manage.py runserver


#makemigrations:
mm:
	poetry run python backend/manage.py makemigrations


#migrate:
mi:
	poetry run python backend/manage.py migrate


#makemigrations and migrate:
ms: mm mi;

#create superuser:
csu:
	poetry run python backend/manage.py createsuperuser



#django shell:
shell:
	poetry run python backend/manage.py shell

#test:
t:
	poetry run pytest

#dumpdata:
dd:
	poetry run python backend/manage.py dumpdata > whole.json


#loaddata:
ld:
	poetry run python backend/manage.py loaddata whole.json

# docker compose
docker-c-up:
	docker-compose -f docker-compose.dev.yml up --force-recreate db
