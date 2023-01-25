# VaccineAvailability

#### python version 3.10.6

#### setup packages

pip install poetry
poetry install

(to install any additional package)
poetry add <package-name>

git config --local blame.ignoreRevsFile .git-blame-ignore-revs
pre-commit autoupdate
pre-commit install
pre-commit install --hook-type commit-msg

#### Steps for execution:

1. Clone the project and create a venv for python.
1. Run commands from setup packages to install required libraries.
1. run `python manage.py collectstatic`
1. Refer https://django-tenants.readthedocs.io/en/latest/use.html to follow the process correctly.
1. Execute command from project directory `daphne -b 0.0.0.0 -p 8000 VaccineAvailability.asgi:application`
