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
#make i -pre-commit
i-pre-commit:
	poetry run pre-commit install

#uninstalling pre-commit
#make u -pre-commit
u-pre-commit:
	poetry run pre-commit uninstall

#updating pre-commit
#make up -pre-commit
up-pre-commit: u-pre-commit i-pre-commit


#installing dependencies
#make -i
-i:
	poetry install

#runserver:
#make rs
rs:
	poetry run python backend/manage.py runserver


#makemigrations:
#make mm
mm:
	poetry run python backend/manage.py makemigrations


#migrate:
#make m
mi:
	poetry run python backend/manage.py migrate


#migrate and make migrations:
#make ms
ms: mm mi;

#create superuser:
#make csu
csu:
	poetry run python backend/manage.py createsuperuser

#django shell:
#make shell
shell:
	poetry run python backend/manage.py shell

#test:
#make t
t:
	poetry run pytest
