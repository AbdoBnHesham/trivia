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

Or with the flask migration package, but make sure you have added .env file in flaskr directory

```bash
flask db upgrade
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

1. [x] Use Flask-CORS to enable cross-domain requests and set response headers.
2. [x] Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint
   should return a list of questions, number of total questions, current category, categories.
3. [x] Create an endpoint to handle GET requests for all available categories.
4. [x] Create an endpoint to DELETE question using a question ID.
5. [x] Create an endpoint to POST a new question, which will require the question and answer text, category, and
   difficulty score.
6. [x] Create a ~~POST~~ GET endpoint to get questions based on category.
7. [x] Create a POST endpoint to get questions based on a search term. It should return any questions for whom the
   search term is a substring of the question.
8. [x] Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous
   question parameters and return a random questions within the given category, if provided, and that is not one of the
   previous questions.
9. [x] Create error handlers for all expected errors including 400, 404, 422 and 500.

## API Documentations

Endpoints GET '/api/categories' GET ''
POST ... DELETE ...

- GET `/api/categories`
    - Fetches a dictionary of categories in which the keys are the ids, and the value is the corresponding string of the
      category
    - Request Arguments: None

Example:

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

---

- GET `/api/questions`
    - Fetches a dictionary of questions, total questions, current category, and categories this serve as main point for
      the application.
    - It's paginated, and returns 10 questions per page
    - Request Arguments:
        - page: type integer

Example:

```json
{
  "categories": {
    "1": "science",
    "2": "art"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 1,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "total_questions": 19
}
```

---

- DELETE `/api/questions/<id>`
    - Delete a question.
    - Request Arguments: None
    - Return 204 for success and 404 if not exists or 500 for server errors.

---

- POST `/api/questions`
    - Create a new question.
    - Request Data:
        - question type string, required.
        - answer type string, required.
        - category type integer, required and should be existed in categories.
        - difficulty type integer, required and should be between 1 and 5.
    - Return 201 and id for success and 422 with a message for errors in validation and 500 for server errors.

---

- POST `/api/questions/serach`
    - Search in questions
    - Request Data:
        - q type string, for search term
        - page type integer

#### Example:

Request Data:

```json
{
  "q": "ind"
}
```

Response:

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 10,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 11,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "total_questions": 2
}
```

---

- GET `/api/categories/<id>/questions`
    - Get questions by category id.
    - Request Arguments:
        - page type integer
    - Return 404 if category doesn't exist

Example:

```json
{
  "current_category": "1",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 16,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "total_questions": 3
}
```

---

- POST `/api/quizzes`
    - Start a quiz
    - Request Data:
        - quiz_category type integer, not required but if provided it should be existing category id.
        - previous_questions type array of integers, ids of previously sent questions.
    - Return a question that doesn't duplicate with previous_questions and from the quiz_category if requested.

Example:

```json
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 17,
    "question": "Who discovered penicillin?"
  }
}
```

## Testing

To run the tests, run

```bash
# You need to specify DB_NAME in your .env
## There is no need to do that as tests 
## will update db with migrations data before each test 
## and remove everything after
## but you will need to add .env.test with
#psql YOUR_DB_NAME < trivia.psql 

# run from the main repository directory
python -m backend.test_flaskr
```