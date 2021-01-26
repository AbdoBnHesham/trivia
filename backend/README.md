# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in
the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for
each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in
the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Quick start

```bash
# create virtual env
python3 -m venv venv
# activate virtual env
source venv/bin/activate 
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies and running:

```bash
# install packages
pip3 install -r backend/requirements.txt
```

This will install all the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](https://flask.palletsprojects.com)  is a lightweight backend microservices framework. Flask is required to
  handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite
  database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest) is the extension we'll use to handle cross origin requests
  from our frontend server.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest) is an extension to handle database migrations versions

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < backend/trivia.psql
```

## Running the server

Before starting development make a copy of .env.example in backend/flaskr/.env as it will be the main point for getting
secret data like SECRET_KEY and DB URI parameters

```bash
cp backend/flaskr/.env.example backend/flaskr/.env
```

From within the main directory first ensure you are working using your created virtual environment. There is no need to
export FLASK_APP and FLASK_ENV because it's already set in .flaskenv

To run the server, execute:

```bash
flask run
```

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data.
The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats
already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or
you will get some unexpected behavior.

1. [ ] Use Flask-CORS to enable cross-domain requests and set response headers.
2. [ ] Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint
   should return a list of questions, number of total questions, current category, categories.
3. [ ] Create an endpoint to handle GET requests for all available categories.
4. [ ] Create an endpoint to DELETE question using a question ID.
5. [ ] Create an endpoint to POST a new question, which will require the question and answer text, category, and
   difficulty score.
6. [ ] Create a POST endpoint to get questions based on category.
7. [ ] Create a POST endpoint to get questions based on a search term. It should return any questions for whom the
   search term is a substring of the question.
8. [ ] Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous
   question parameters and return a random questions within the given category, if provided, and that is not one of the
   previous questions.
9. [ ] Create error handlers for all expected errors including 400, 404, 422 and 500.

REVIEW_COMMENT

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Testing

To run the tests, run

```bash
# You need to specify DB_NAME in your .env
psql YOUR_DB_NAME < trivia.psql
# run from the main repository directory
python -m backend.test_flaskr
```