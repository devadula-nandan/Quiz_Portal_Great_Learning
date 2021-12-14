from enum import unique
from marshmallow.schema import Schema
from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func

"""
[DataBase Access Details]
Below is the configuration mentioned by which the application can make connection with MySQL database
"""
username = 'root'
password = 'nandan123'
database_name = 'quiz_app'
application.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{username}:{password}@localhost/{database_name}"
# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)


class UserMaster(db.Model):
    __tablename__ = 'user_master'
    id = Column(String(100), primary_key=True)
    name = Column(String(200))
    username = Column(String(200), unique=True)
    password = Column(String(200))
    is_admin = Column(Integer)
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())


def __init__(self, id, name, username, password, is_admin, is_active, created_ts, updated_ts):
    self.id = id
    self.name = name
    self.username = username
    self.password = password
    self.is_admin = is_admin
    self.is_active = is_active
    self.created_ts = created_ts
    self.updated_ts = updated_ts


class UserSession(db.Model):
    __tablename__ = 'user_session'
    id = Column(String(100), primary_key=True)
    user_id = Column(String(200), ForeignKey("user_master.id"))
    session_id = Column(String(200), unique=True)
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, user_id, session_id, is_active, created_ts, updated_ts):
        self.id = id
        self.user_id = user_id
        self.session_id = session_id
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


class QuestionMaster(db.Model):

    __tablename__ = 'question_master'
    id = Column(String(100), primary_key=True)
    question = Column(String(500))
    choice1 = Column(String(500))
    choice2 = Column(String(500))
    choice3 = Column(String(500))
    choice4 = Column(String(500))
    answer = Column(Integer)
    marks = Column(Integer)
    remarks = Column(String(200))
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, question, choice1,
                 choice2, choice3, choice4, answer, marks, remarks, is_active, created_ts, updated_ts):
        self.id = id
        self.question = question
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3
        self.choice4 = choice4
        self.answer = answer
        self.marks = marks
        self.remarks = remarks
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


class QuizMaster(db.Model):

    __tablename__ = 'quiz_master'
    id = Column(String(100), primary_key=True)
    quiz_name = Column(String(200))
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, quiz_name, is_active, created_ts, updated_ts):
        self.id = id
        self.quiz_name = quiz_name
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


class QuizQuestions(db.Model):

    __tablename__ = 'quiz_questions'
    __table_args__ = (
        db.UniqueConstraint('quiz_id', 'question_id',
                            name='unique_quiz_question'),
    )

    id = Column(String(100), primary_key=True)
    quiz_id = Column(String(200), ForeignKey("quiz_master.id"))
    question_id = Column(String(200), ForeignKey("question_master.id"))
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, quiz_id, question_id, is_active, created_ts, updated_ts):
        self.id = id
        self.quiz_id = quiz_id
        self.question_id = question_id
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


class QuizInstance(db.Model):
    __tablename__ = 'quiz_instance'
    __table_args__ = (
        db.UniqueConstraint('quiz_id', 'user_id', name='unique_quiz_user'),
    )

    id = Column(String(100), primary_key=True)
    quiz_id = Column(String(200), ForeignKey("quiz_master.id"))
    user_id = Column(String(200), ForeignKey("user_master.id"))
    score_achieved = Column(Integer)
    is_submitted = Column(Integer)
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, quiz_id, user_id, score_achieved, is_submitted, is_active, created_ts, updated_ts):
        self.id = id
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.score_achieved = score_achieved
        self.is_submitted = is_submitted
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


class UserResponses(db.Model):
    __tablename__ = 'user_responses'
    __table_args__ = (
        db.UniqueConstraint('quiz_id', 'user_id', 'question_id',
                            name='unique_quiz_user_question'),
    )

    id = Column(String(100), primary_key=True)
    quiz_id = Column(String(200), ForeignKey("quiz_master.id"))
    user_id = Column(String(200), ForeignKey("user_master.id"))
    question_id = Column(String(200), ForeignKey("question_master.id"))
    response = Column(Integer)
    is_active = Column(Integer)
    created_ts = Column(DateTime(timezone=True), server_default=func.now())
    updated_ts = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, id, quiz_id, user_id, question_id, response, is_active, created_ts, updated_ts):
        self.id = id
        self.quiz_id = quiz_id
        self.user_id = user_id
        self.question_id = question_id
        self.response = response
        self.is_active = is_active
        self.created_ts = created_ts
        self.updated_ts = updated_ts


db.create_all()
db.session.commit()
