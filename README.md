![Screenshot](https://img.shields.io/badge/python-v3.10-blue?logo=python&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/postgresql-v15-blue?logo=postgresql&logoColor=yellow)
![Screenshot](https://img.shields.io/badge/sqlalchemy--blue)
![Screenshot](https://img.shields.io/badge/rich--blue)
![Screenshot](https://img.shields.io/badge/betterstack--blue)

# [OpenClassRoom](https://openclassrooms.com/) - Parcours développeur Python
![Screenshot](illustrations/oc_parcours_dev_python.png)
## Projet 12 - Créer un backend sécurisé en utilisant Django ORM

### Project description
    Create a cli console "Customer Relationship Management" application with Python.
    Context is an event organization dedicated application.
    Company has several departments: commercial, gestion, support.
    Commercial will look for clients. They try to sign contracts for an event.
    Once contract signed, the gestion team assign a support collaborator to the event.


### Requirements
    Python >= 3.10
    Supply a database scheme.
    Use an ORM (SQLALCHEMY).
    Any of these SGBD: SQLite, MySQL, PostgreSQL.
    Propose a graphical admin tool dedicated to the SGBD (pgadmin, MySQLWorkbench, etc)
    Secure authentication with JWT.
    Use Click python's package.
    Supply a Sentry's like log monitoring capability. Grab any of these elements:
      - all unexpected exceptions
      - any creation or update for a collaborator
      - any contract signature


### Competencies assessed
    Create a "Customer Relationship Management" like application
    Set a secured database with Python and SQL

---

### Project setup
    Application have been developed on a Linux system. The choosen SGBD is Postgresql (version 15).
    Initialization of application needs to run several command as admin on the SGBD, see: src/commands/init_commands.py
    On Linux these commands are run with sudo.
    For Windows user, use Windows 10 or later, and activate the bash usage on it. You can offcourse update the code as an improvement.

    Application initialization will create 3 databases named: projet12, dev_projet12. et test_projet12 (prod, dev and test environment).
    In each one you will have the 3 companies departments expected in specifications: oc12_commercial, oc12_gestion et oc12_support.
    Also 7 collaborators will be created: 2 commercial, 2 gestion, and 3 gestion members.
    A collaborator belongs to 1 department.

    Accounts: a123456789, ab123456789, ..., ag123456789.
    Default password is specify in settings, you can change it. By default the user password is: @pplepie94.
    Each user has only 1 account ("role", according to Postgresql terminology) to access the 3 databases.
    So a password update would concern any environment.

    The Dev and Test databases will be populated with more datas (clients, companies, contracts, events).
    The Test database is dedicated to be used by pytest.

---

### About authentication and authorizations
    As explained and illustrated below, users will have to obtain a JWT Token in order to use application.
    To obtain the token or to update the password, use will use his credential.

    The token will specify the collaborator's service: it is the service which owns the grant on database.
    Users will inheritate all of his service's authorizations.

    One exception concerns the "Gestion service" whose members must be able to create, delete, update an user.
    In our Postgresql context, we have to set the specific grant "Create Role" to any member of this service.
    This grant won't be inheritated.
   [Postgresql doc](https://www.postgresql.org/docs/current/sql-createrole.html)

---

### Database administration
    Optional. As a graphical tool to administrate database, pgadmin4 can be used for Postgresql.
    Illustration in the wiki page:
   [OC12 WIKI](https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm/wiki)

---

### How works this project ?

Notice the Wiki page created for this project, from Github: [OC12 WIKI](https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm/wiki)

    Any commands you could /should be consult with command "oc12_help".

|COMMAND|INFO|
|-------|----|
|oc12_init_application| initialize application|
|oc12_token| obtain an access token|
|oc12_clients| obtain all clients of the company|
|oc12_contracts --help| obtain help for command oc12_contracts|
|oc12_contracts "status=signed et remain_amount_to_pay =>0"| usecase example for a filter query|
|oc12_update_event --event_id=geg2021 collaborator_id=af123456789|usecase example for update event|
|oc12_update_event --event_id=geg2021 collaborator_id=None|usecase example for update event|
|oc12_events 'commercial_id=aa123456789 ou commercial_id=ab123456789'|usecase example for filter events looking for 2 assigned collaborators|
|(...)||

    Notice: all commands can be prefixed too by "poetry run". Example: "poetry run get_clients" etc.

    Furthermore you may be restricted by the native application rules, at any time.
    Most of them should be intuitive (by the Foreign keys dependencies).
    From now you may consider, for example:
      - To query application you need a JWT token exported in your PATH.
      - Before query a JWT token, you first need to declare the application environment in your PATH.
      - To obtain a JWT token you will use command 'oc12_token' as precise through 'oc12_help'.
      - 1 collaborator has 1 service /department and 1 role (manager, employee etc).
      - 1 company depends on an existing location.
      - Any instance model can be filtered as soon as user allowed to query.
      - Any instance model comes with a(n implicit) creation date.
Please consult all implemented rules in the wiki project page [OC12 WIKI](https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm/wiki)

As the application is set to be connected to internet the following API's are used:

- https://recherche-entreprises.api.gouv.fr

- https://geo.api.gouv.fr

Notice that **log collect is activated by default**. You can deactivate it through settings file (INTERNET_CONNECTION and LOG_COLLECT_ACTIVATED to False).

---

### How use this project ?

  1. Clone the repository

      `git clone https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm.git`

      `cd oc_projet12_backend_securise_avec_django_orm`

  2. Set a .envrc file

      You must create a .envrc file with this **example** content.
      If you want to collect logs on Betterstack, you have to set the BETTERSTACK_SOURCE_TOKEN.
      If you don't want to collect logs, you don't need to set it.

            SECRET_KEY='MakeYourOwnSecretKey'
            ADMIN_LOGIN='admin'
            ADMIN_PASSWORD='admin'
            OC12_COMMERCIAL_PWD='MakeItStrong'
            OC12_GESTION_PWD='MakeItSecured'
            OC12_SUPPORT_PWD='MakeItGreat'
            BETTERSTACK_SOURCE_TOKEN='SuperTokenFromBetterStack'

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

      Notice application has been run on a Linux operating system. Some commands will relied on it.

      First in a Linux running context, deactivate any input into history: `set -o history` (this will apply for the terminal session duration). This is optional.

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

### Simple usecases illustrated
[OC12 WIKI](https://github.com/memphis-tools/oc_projet12_backend_securise_avec_django_orm/wiki/OpenClassRoom-Project-12-%E2%80%90-Parcours-utilisateur-pour-soutenance)
