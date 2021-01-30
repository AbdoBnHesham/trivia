import os
import unittest
from pathlib import Path

from flask.wrappers import Response
from flask_migrate import Migrate, upgrade, downgrade
from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import setup_db, Question, Category

backend_path = Path(__file__).parent
migrations_path = Path(backend_path, 'migrations')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_env='.env.test')
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = setup_db(self.app, {
                'name': os.getenv('DB_NAME')
            })
            self.f_migrate = Migrate(self.app, self.db, directory=migrations_path)
            upgrade(directory=migrations_path)

    def tearDown(self):
        """Executed after reach test"""
        # drop all tables after finishing
        with self.app.app_context():
            downgrade(directory=migrations_path)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_can_get_all_categories(self):
        res: Response = self.client().get('/api/categories')
        res_data: dict = res.get_json()
        categories: dict = res_data.get('categories')

        self.assertEqual(res.status_code, 200, "Response status code isn't 200 ok")
        self.assertTrue(isinstance(categories, dict), "Categories aren't a dictionary")
        self.assertEqual(categories['1'], 'science', "Initial categories aren't exist")

    def test_can_get_questions(self):
        res: Response = self.client().get('/api/questions')
        res_data: dict = res.get_json()
        questions: list[dict] = res_data.get('questions')
        total_questions: int = res_data.get('total_questions')
        categories: dict = res_data.get('categories')
        current_category: int = res_data.get('current_category')

        # request status
        self.assertEqual(res.status_code, 200, "Response status code isn't 200 ok")

        # questions format
        self.assertTrue(isinstance(questions, list), "Questions are not a dictionary")
        for k in ['id', 'question', 'answer', 'category', 'difficulty']:
            self.assertTrue(k in questions[0].keys())
            self.assertTrue(questions[0] is not None)

        # categories format
        self.assertTrue(isinstance(categories, dict), "Categories aren't a dictionary")

        # values
        self.assertEqual(current_category, None, 'Current category should be empty when requesting all')
        self.assertEqual(len(questions), 10, "Total Questions per page isn't 10")
        self.assertEqual(total_questions, 19, 'Question total are not 19')

    def test_can_get_another_page_of_questions(self):
        res: Response = self.client().get('/api/questions?page=2')
        res_data: dict = res.get_json()
        questions: list[dict] = res_data.get('questions')

        self.assertEqual(len(questions), 9, "Total Questions per page isn't 9 on the second page")

    def test_cant_get_not_existing_page_of_questions(self):
        res: Response = self.client().get('/api/questions?page=2000')
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 404, "Response status code isn't 404 not found.")
        self.assertEqual(res_data.get("message"), "Not found.", "Response doesn't have message with Not found")

    def test_can_delete_question_by_id(self):
        _id = 1
        res: Response = self.client().delete(f"/api/questions/{_id}")

        with self.app.app_context():
            question_exists = self.db.session.query(Question.query.filter_by(id=_id).exists()).scalar()
        self.assertFalse(question_exists, "Question still exists after deletion")
        self.assertEqual(res.status_code, 204, "Response status code isn't 204 no content")

    def test_cant_delete_question_by_id_with_not_existing_id(self):
        _id = 100000
        res: Response = self.client().delete(f"/api/questions/{_id}")
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 404, "Response status code isn't 404 not found")
        self.assertEqual(res_data.get("message"), "Not found.", "Response doesn't have message with Not found")

    def test_can_create_a_new_question(self):
        data = {
            "question": "When did the French Revolution end?",
            "answer": "1799",
            "category": 4,
            "difficulty": 2,
        }
        res: Response = self.client().post("/api/questions", json=data)
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 201, "Response status code isn't 201 created")
        _id = res_data.get('id')
        with self.app.app_context():
            question: Question = Question.query.get(_id)
        self.assertTrue(question, "Question doesn't exist")
        self.assertEqual(question.question, data['question'], "Question doesn't exist")
        self.assertEqual(question.answer, data['answer'], "Question doesn't exist")
        self.assertEqual(question.category_id, data['category'], "Question doesn't exist")
        self.assertEqual(question.difficulty, data['difficulty'], "Question doesn't exist")

    def test_cant_create_a_new_question_without_any_field(self):
        data = {}
        res: Response = self.client().post("/api/questions", json=data)
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 422, "Response status code isn't 422 unprocessable entity")
        message = "There is an empty required field. Category doesn't exist. Difficulty range is between 1 to 5."
        self.assertEqual(res_data.get('message'), message)

    def test_cant_create_a_new_question_with_not_existing_category_id(self):
        data = {
            "question": "When did the French Revolution end?",
            "answer": "1799",
            "category": 4000,
            "difficulty": 2,
        }
        res: Response = self.client().post("/api/questions", json=data)
        res_data: dict = res.get_json()
        self.assertEqual(res.status_code, 422, "Response status code isn't 422 unprocessable entity")
        message = "Category doesn't exist. "
        self.assertEqual(res_data.get('message'), message)

    def test_cant_create_a_new_question_with_a_difficulty_out_of_1_to_5_range(self):
        # less than 1
        data = {
            "question": "When did the French Revolution end?",
            "answer": "1799",
            "category": 4,
            "difficulty": -1,
        }
        res: Response = self.client().post("/api/questions", json=data)
        res_data: dict = res.get_json()
        self.assertEqual(res.status_code, 422, "Response status code isn't 422 unprocessable entity")
        message = "Difficulty range is between 1 to 5."
        self.assertEqual(res_data.get('message'), message)

        # more than 5
        data['difficulty'] = 6
        res: Response = self.client().post("/api/questions", json=data)
        res_data: dict = res.get_json()
        self.assertEqual(res.status_code, 422, "Response status code isn't 422 unprocessable entity")
        message = "Difficulty range is between 1 to 5."
        self.assertEqual(res_data.get('message'), message)

    def test_can_search_questions(self):
        data = {
            "q": "Indian"
        }
        res: Response = self.client().post("/api/questions/search", json=data)
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 200, "Response status code isn't 200 ok")

        self.assertTrue(res_data.get('questions'), "Questions doesn't exist")
        self.assertEqual(len(res_data.get('questions')), 1, "Total Questions per page isn't 1")
        self.assertEqual(res_data.get('total_questions'), 1, 'Question total are not 1')

        self.assertEqual(res_data.get('current_category'), None)  # TODO search more about it's usage

    def test_can_search_with_a_word_doesnt_exist_questions(self):
        data = {
            "q": "Something you can't get a question about"
        }
        res: Response = self.client().post("/api/questions/search", json=data)
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 200, "Response status code isn't 200 ok")

        self.assertTrue('questions' in res_data.keys(), "Questions doesn't exist")
        self.assertEqual(len(res_data.get('questions')), 0, "Total Questions per page isn't 0")
        self.assertEqual(res_data.get('total_questions'), 0, "Question total isn't 0")

        self.assertEqual(res_data.get('current_category'), None)  # TODO search more about it's usage

    def test_can_get_questions_by_category(self):
        _id = 1
        res: Response = self.client().get(f"/api/categories/{_id}/questions")
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 200, "Response status code isn't 200 ok")
        self.assertTrue('questions' in res_data.keys(), "Questions doesn't exist")
        self.assertEqual(len(res_data.get('questions')), 3, "Total Questions per page isn't 3")
        self.assertEqual(res_data.get('total_questions'), 3, "Category's question total are not 3")

        self.assertEqual(
            int(res_data.get('current_category')), _id,
            "Current category isn't equal to requested category id"
        )

    def test_cant_get_questions_by_category_doesnt_exist(self):
        _id = 1000
        res: Response = self.client().get(f"/api/categories/{_id}/questions")
        res_data: dict = res.get_json()

        self.assertEqual(res.status_code, 404, "Response status code isn't 404 not found")
        self.assertEqual(res_data.get("message"), "Not found.", "Response doesn't have message with Not found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
