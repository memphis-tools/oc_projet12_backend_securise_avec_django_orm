![Screenshot](python-sqlalchemy.svg)
# [OpenClassRoom](https://openclassrooms.com/) - Parcours développeur Python
![Screenshot](oc_parcours_dev_python.png)
## Projet 12 - Créer un backend sécurisé en utilisant Django ORM

### Project description
    Create a console "Customer Relationship Management" application with Python.
    Context is an event organization dedicated application.
    Company has several departments: commercial, gestion, support.
    Commercial will look for clients. They try to sign contracts for an event.
    Once contract signed, the gestion team assign a support collaborator to the event.
    For 1 event, we have 1 client, 1 commercial and 1 support collaborator.


### Requirements
    Python >= 3.9
    Supply a database scheme.
    Use an ORM.
    Secure authentication with JWT.
    Supply a Sentry's log monitoring from application usage.


### Competencies assessed
    Set a secured database with Python and SQL

---

## How works this project ?
    Any commands you could /should consult in with "--help".

    |COMMAND|INFO|
    |-------|----|
    |get_clients| GET all clients|
    |get_contracts| GET all contracts|
    |||

    Notice: all commands can be prefixed too by "poetry run". Example: "poetry run get_clients" etc.

---

## How use this project ?

  1. Clone the repository

      `git clone https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm.git`

      `cd oc_projet12_backend_securise_avec_django_orm`

  2. Set a .envrc file

      You must create a .envrc file with this content.

            SECRET_KEY='MakeYourOwnSecretKey'
            ADMIN_LOGIN='admin'
            ADMIN_PASSWORD='admin'

      To make your own secret_key use module secrets.

            >>> import secrets
            >>> secrets.token_hex()
            'e2b4968b3f0172325702bbfa292d0d99b07bee22e3ab312e5855beb9151a379d'

  3. Setup the virtualenv

     `poetry install`

      Update any modules.

      `poetry update`

      You should have a ".venv" created. First we update the prompt for user experience.

      `poetry config virtualenvs.prompt oc_projet12`

      Then source the .venv either way like following:

      `source $(poetry env info --path)/bin/activate`

      or

      `source .venv/bin/activate`

  4. Instantiate database and inject dummy data for the POC purposes

      `poetry run launch_application`

     or

     `launch_application`

  6. Optional

      Run tests and check cover stats.

      `python -m coverage run -m pytest -v`

      `python -m coverage report`

      Check flake8:

      `poetry run flake8 --format html --htmldir flake8_report`
