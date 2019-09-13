# HairQ API

[![Coverage Status](https://coveralls.io/repos/github/d-kahara/hairq-API/badge.svg?branch=master)](https://coveralls.io/github/d-kahara/hairq-API?branch=master)
## Development set up

#### Set up with docker
###### todo Update this section


#### Set up without docker

- Check that python 3, pip, virtualenv and postgress are installed

- Clone the hairq-api repo and cd into it
    ```
    git clone https://github.com/d-kahara/hairq-API.git
    ```
- Create virtual env
    ```
    virtualenv --python=python3 venv
    ```
- Activate virtual env
    ```
    source venv/bin/activate
    ```
- Install dependencies
    ```
    pip install -r requirements.txt
    ```
- Create Application environment variables and save them in .env file
    ```
    export APP_SETTINGS="development" # set app Enviroment.
    export SECRET_KEY="some-very-long-string-of-random-characters"
    export DEV_DATABASE_URL="" # Db for Development.
    export TEST_DATABASE_URL="" # Db for Testing
    export DATABASE_URL="" # Db for Production
    ```
- Running migrations

    - Initial migration commands
        ```
        $ alembic revision --autogenerate -m "Migration message"

        $ alembic upgrade head
        ```
    - If you have one migration file in the alembic/version folder. Run the commands below:
        ```
        $ alembic stamp head

        $ alembic upgrade head
        ```
    - If you have more than 2 migration files in the alembic/versions folder. Rum the commands bellow
        ```
        $ alembic stamp head

        $ alembic upgrade head

        $ alembic revision --autogenerate -m "Migration message"

        $ alembic upgrade head

        ```


- Run application.
    ```
    python manage.py runserver
    ```

- Running Tests

 ```
 coverage run -m pytest
 ```
 - To obtain coverage report. Run the command below:

 ```
 coverage report
 ```
 - To obtain html browser report. Run command below:
 ```
 coverage html
 ```
 ```
 A folder titled html_coverage_report will be generated. Open it and copy the path  of index.html and paste it in your browser.
 ```

## Built with
- Python version  3
- Flask
- Grapghql
- Postgres
