import os

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import (
    Column, String,
    Integer, ForeignKey
)

db = SQLAlchemy()


def setup_db(app, db_secrets=None):
    """
    setup_db(app)
        binds a flask application and a SQLAlchemy service
    """
    if not db_secrets:
        print(' $ IMPORTANT There is no value for DB URI, using sqlite in memory')
        db_uri = 'sqlite:///:memory:'
    else:
        user = db_secrets.get('user', os.getenv('DB_USER'))
        _pass = db_secrets.get('pass', os.getenv('DB_PASS', ''))
        host = db_secrets.get('host', 'localhost')
        port = db_secrets.get('port', '5432')
        db_name = db_secrets.get('name')
        db_uri = f"postgresql://{user}:{_pass}@{host}:{port}/{db_name}"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    return db


class Question(db.Model):
    """
    Question

    """
    query: BaseQuery

    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category_id = Column(
        Integer,
        ForeignKey('categories.id', ondelete='CASCADE')
    )
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    # noinspection PyMethodMayBeStatic
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """
    Category

    """
    query: BaseQuery

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = db.relationship(
        'Question',
        lazy=True,
        backref=db.backref('category', lazy=False, cascade='all, delete')
    )

    # noinspection PyShadowingBuiltins
    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
