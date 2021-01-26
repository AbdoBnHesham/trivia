import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from .flaskr import create_app
from .models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config={
            'ENV': 'TESTING',
            'TESTING': True,
        })
        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = setup_db(self.app, {
                'db_name': os.getenv('DB_TEST_NAME')
            })
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        # drop all tables after finishing
        self.db.drop_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
