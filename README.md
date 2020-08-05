#### This code was edited. Source credited n copyright: Faviansyah Arianda Pallas (https://github.com/favians)

# Starter python for REST API

this project using this kind of library:
* API Framework : https://www.fullstackpython.com/flask.html
* ORM : https://flask-sqlalchemy.palletsprojects.com/en/2.x/
* Configs : https://pypi.org/project/python-dotenv/
* Unit Test : https://docs.pytest.org/en/latest/
* Logging : https://docs.python.org/2/library/logging.html

#### How to Start Project
1. Clone this project:
```git clone https://github.com/favians/python_restAPI_starter.git```
2. Create env:
```python3 -m venv env```
3. Activate ENV:
```source env/bin/activate```
4. install requirements:
```pip install -r requirements.txt```
5. configure your env in .env file
6. migrate the database:
```python3 app.py db migrate```
7. upgrade database:
```python3 app.py db upgrade```
8. run the program:
```python3 app.py```

#### Run with Docker Compose
```docker-compose up```
