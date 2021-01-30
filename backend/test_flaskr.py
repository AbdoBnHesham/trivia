import os
import unittest
import json
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
        res_data: dict = json.loads(res.data)
        categories: dict = res_data.get('categories')

        self.assertEqual(res.status_code, 200, "Request status code isn't 200 ok")
        self.assertTrue(isinstance(categories, dict), "Categories aren't a dictionary")
        self.assertEqual(categories['1'], 'science', "Initial categories aren't exist")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
