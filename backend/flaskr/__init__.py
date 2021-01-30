import os
from pathlib import Path
from re import match

from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from backend.models import setup_db, Category, Question

flaskr_dir_path = Path(__file__).parent
QUESTIONS_PER_PAGE = 10


def create_app(test_env: str = None):
    """
    create and configure the app
    @type test_env: str relative path for .env or .env.test from __init__.py
    """

    app = Flask(__name__)
    if test_env is None:
        # load the instance config, from app settings environment variable if not testing
        app.config.from_envvar('APP_SETTINGS')
    else:
        # load the test env file if passed in
        app.config.from_pyfile(test_env)

    # making sure .env file is loaded for db and other modules
    env_path = Path(flaskr_dir_path, test_env or '.env').absolute()
    load_dotenv(env_path)

    db = setup_db(app, {
        'name': os.getenv('DB_NAME')
    })

    Migrate(
        app, db,
        # to make sure migrations inside backend folder
        directory=Path(flaskr_dir_path.parent, 'migrations').absolute()
    )

    # @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    cors = CORS(app, resources={
        r"^/api/*": {'origin': '*'},
    })

    # @DONE: Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response: Response):
        if match(r'^/api/*', request.path):  # to make sure it's only allowed for api endpoints
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE')
        return response

    @app.route('/api/categories')
    def get_all_categories():
        """
        @DONE:
        Create an endpoint to handle GET requests
        for all available categories.
        """
        categories = Category.query.all()

        res = {
            'categories': {c.id: c.type for c in categories}
        }

        return jsonify(res)

    @app.route('/api/questions')
    def get_questions():
        """
        @DONE:
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.

        TEST: At this point, when you start the application
        you should see questions and categories generated,
        ten questions per page and pagination at the bottom of the screen for three pages.
        Clicking on the page numbers should update the questions.
        """

        questions = Question.query.paginate(per_page=QUESTIONS_PER_PAGE)
        categories = Category.query.all()

        data = {
            'questions': [q.format() for q in questions.items],
            'total_questions': questions.total,
            'categories': {c.id: c.type for c in categories},
            'current_category': None,
        }

        return jsonify(data)

    @app.route('/api/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        @DONE:
        Create an endpoint to DELETE question using a question ID.

        TEST: When you click the trash icon next to a question, the question will be removed.
        This removal will persist in the database and when you refresh the page.
        """

        question = Question.query.get_or_404(question_id)
        try:
            db.session.delete(question)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            db.session.close()
            return '', 500

        return '', 204

    @app.route('/api/questions', methods=['POST'])
    def add_question():
        """
        @TODO:
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        TEST: When you submit a question on the "Add" tab,
        the form will clear and the question will appear at the end of the last page
        of the questions list in the "List" tab.
        """

        data: dict = request.get_json()

        question = data.get('question')
        answer = data.get('answer')
        category = data.get('category')
        difficulty = int(data.get('difficulty', 0))

        all_values_exist = all([question, answer, category, difficulty])
        category_exist = db.session.query(Category.query.filter_by(id=category).exists()).scalar()
        difficulty_in_range = 1 <= difficulty <= 5

        if not all([all_values_exist, category_exist, difficulty_in_range]):
            message = ""
            if not all_values_exist:
                message = "There is an empty required field. "
            if not category_exist:
                message += "Category doesn't exist. "
            if not difficulty_in_range:
                message += "Difficulty range is between 1 to 5."
            return jsonify({
                'message': message
            }), 422

        question_model = Question(
            question=question,
            answer=answer,
            category_id=category,
            difficulty=difficulty
        )

        try:
            db.session.add(question_model)
            db.session.commit()
            _id = question_model.id
        except SQLAlchemyError:
            db.session.rollback()
            db.session.close()
            return '', 500

        return jsonify({
            'id': _id,
        }), 201

    @app.route('/api/questions/search', methods=['POST'])
    def search_question():
        """
        @DONE:
        Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.

        TEST: Search by any phrase. The questions list will update to include
        only question that include that string within their question.
        Try using the word "title" to start.
        """
        q = request.get_json().get('q', '')
        questions = Question.query.filter(
            Question.question.ilike(f"%{q}%")
        ).paginate(per_page=QUESTIONS_PER_PAGE)

        data = {
            'questions': [q.format() for q in questions.items],
            'total_questions': questions.total,
            'current_category': None,
        }

        return jsonify(data)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "message": "Not found.",
        }), 404

    return app
