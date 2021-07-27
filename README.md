# Starter python for REST API

this project using this kind of library:
* API Framework : https://www.fullstackpython.com/flask.html
* ORM : https://flask-sqlalchemy.palletsprojects.com/en/2.x/
* Configs : https://pypi.org/project/python-dotenv/
* Unit Test : https://docs.pytest.org/en/latest/
* Logging : https://docs.python.org/2/library/logging.html

#### How to Start Project
1. Clone this project:
    ```git clone https://github.com/aswindanu/python-flask-starter.git flask_starter```

2. Create env:
    ```python -m venv env```

3. Activate ENV (Linux/OSX):
    ```source env/bin/activate```

4. GO to project dir:
    ```cd flask_starter```

5. install requirements:
    ```pip install -r requirements.txt```

6. configure your env in .env file

    - DEBUG=
    - JWT_SECRET=
    - DATABASE_USER=
    - DATABASE_PASSWORD=
    - DATABASE_HOST=
    - DATABASE_PORT=
    - DATABASE_NAME=

7. initiate the database:
    ```flask db init```

8. migrate the database:
    ```flask db migrate```

9. upgrade database:
    ```flask db upgrade```

10. run the program:
    ```flask run```

#### Run with Docker Compose
```docker-compose up```

#### Update requirements (virtualenv)
```pip freeze -l > requirements.txt```

#### Update Swagger UI (`/api/docs`)

    - Update postman collection
    - Update swagger.json by convert postman using coverter from `https://www.apimatic.io/transformer/` or `https://apitransform.com/`
    - see `<domain>:<port>/api/docs`

#### Reset migration db
delete migrations, then use ```flask db init```

#### (OPT) Windows note
Note for windows can be seen at win_note.txt
