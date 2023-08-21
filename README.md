![Screenshot](python-sqlalchemy.svg)
# [OpenClassRoom](https://openclassrooms.com/) - Parcours développeur Python
![Screenshot](oc_parcours_dev_python.png)
## Projet 12 - Créer un backend sécurisé en utilisant Django ORM

### Project description
    Create a cli console "Customer Relationship Management" application with Python.
    Context is an event organization dedicated application.
    Company has several departments: commercial, gestion, support.
    Commercial will look for clients. They try to sign contracts for an event.
    Once contract signed, the gestion team assign a support collaborator to the event.
    For 1 event, we have 1 client, 1 commercial and 1 support collaborator.


### Requirements
    Python >= 3.9
    Supply a database scheme.
    Use an ORM (SQLALCHEMY).
    Secure authentication with JWT.
    Use Click python's package.
    Supply a Sentry's like log monitoring capability. Grab any of these elements:
      - all unexpected exceptions
      - any creation or update for a collaborator
      - any contract signature


### Competencies assessed
    Set a secured database with Python and SQL

---

### How works this project ?
    Any commands you could /should consult with command "oc12_help".

|COMMAND|INFO|
|-------|----|
|oc12_init_application| initialiser un POC|
|oc12_token| obtenir un jeton d'accès|
|oc12_logout| se déconnecter de l'application|
|oc12_clients| obtenir les clients de l'entreprise|
|oc12_contracts --help| obtenir de l'aide sur la commande oc12_contracts|
|oc12_contracts "status=signed et remain_amount_to_pay =>0"| un exemple d'usage de l'aide pour la commande.|
|(...)||

    Notice: all commands can be prefixed too by "poetry run". Example: "poetry run get_clients" etc.

    Furthermore you may be restricted by the native application rules, at any time.
    Most of them should be intuitive (by the Foreign keys dependencies).
    From now you may consider, for example:
      - To query application you need a JWT token exported in your PATH.
      - To obtain a JWT token you will use command 'oc12_token' as precise through 'oc12_help'.
      - 1 collaborator belongs to 1 service /department.
      - 1 company depends on an existing location.
      - 1 contract depends on an existing company and existing collaborator.
      - Any instance model can be filtered as soon as user allowed to query.
      - Any instance model comes with a(n implicit) creation date.
      etc

As the application is set to be connected to internet the following API's are used:

- https://recherche-entreprises.api.gouv.fr

- https://geo.api.gouv.fr

---

### How use this project ?

  1. Clone the repository

      `git clone https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm.git`

      `cd oc_projet12_backend_securise_avec_django_orm`

  2. Set a .envrc file

      You must create a .envrc file with this **example** content.

            SECRET_KEY='MakeYourOwnSecretKey'
            ADMIN_LOGIN='admin'
            ADMIN_PASSWORD='admin'
            OC12_COMMERCIAL_PWD='MakeItStrong'
            OC12_GESTION_PWD='MakeItSecured'
            OC12_SUPPORT_PWD='MakeItGreat'

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

      We set the poetry cache dir inside the application repository.

      `poetry config cache-dir ./.cache/pypoetry --local`

      Then source the .venv either way like following:

      `source $(poetry env info --path)/bin/activate`

      or

      `source .venv/bin/activate`

  4. Instantiate database and inject dummy data for the POC purposes

      `poetry run oc12_init_application`

     or

     `oc12_init_application`

     *: POC = Proof Of Concept

  5. Start using the application

      Notice application had been run on a Linux operating system. Some commands will relied on it.

      First deactivate any input into history: `set -o history` (this will apply for the terminal session duration). This is optional.

      Then you will need a token access. Valid duration period is set through the settings.py file.

      `oc12_token`

      Without anymore export the only PROD database will be used. Before ask the token, notice that as a Developer perspective:
        - you must also: `export OC_12_ENV="DEV"`.
        - if you have something to test you therefore have to : `export OC_12_ENV="TEST"`.

      If your authentication succeeded you will have a JWT token print into terminal.

      You have to source it in your PATH (be sure to copy/paste a full single line). **Example**:

        `export OC_12_JWT='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCZzzzZZZzzz'`

      Then you should be able to use the application. Use `oc12_help` to learn about possible commands.

      Finally, in a Linux running context, you can retrieve commands in history by running (this is optional):
      `set -o history`

  6. Optional

      Run tests and check cover stats. Run tests and check cover stats.

      `python -m coverage run -m pytest -v`

      `python -m coverage report`

      Check flake8:

      `poetry run flake8 --format html --htmldir flake8_report`

---
