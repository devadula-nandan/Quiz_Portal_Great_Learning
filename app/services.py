from sqlalchemy.orm.session import sessionmaker
from app.models import QuestionMaster, QuizInstance, QuizMaster, QuizQuestions, UserMaster, UserResponses, UserSession
from app import db
import uuid
from flask import session
import datetime
from typing import List

"""
[Services Module] Implement various helper functions here as a part of api
                    implementation using MVC Template
"""


class User():
    @staticmethod
    def sign_up(data):
        username = UserMaster.query.filter_by(username=data['username']).first()
        if not username:
            new_user = UserMaster(
                id=str(uuid.uuid4()),
                name=data['name'],
                username=data['username'],
                password=data['password'],
                is_admin=0,
                is_active=1,
                created_ts=datetime.datetime.utcnow(),
                updated_ts=datetime.datetime.utcnow()
            )
            save_changes(new_user)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 409

    @staticmethod
    def login(data):
        try:
            user = UserMaster.query.filter_by(username=data['username']).first()
            if user.password == data['password']:
                if session['id']:
                    user_session = UserSession.query.filter_by(user_id=user.id).first()
                    session['id'] = user_session.session_id
                    user_session.is_active = 1
                    user_session.updated_ts = datetime.datetime.utcnow()
                    save_changes(user_session)
                else:
                    session['id'] = str(uuid.uuid4())
                    new_session = UserSession(
                        id=str(uuid.uuid4()),
                        user_id = user.id,
                        session_id=session['id'],
                        is_active= 1,
                        created_ts=datetime.datetime.utcnow(),
                        updated_ts=None
                    )
                    save_changes(new_session)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.'
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout():
        if session['id']:
            user_session = UserSession.query.filter_by(session_id=session['id']).first()
            user_session.is_active = 0
            user_session.updated_ts = datetime.datetime.utcnow()
            session['id'] = None
            save_changes(user_session)
            response_object = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'session is empty, to logout'
            }
            return response_object, 401

    @staticmethod
    def get_all():
        return UserMaster.query.all()

    @staticmethod
    def get_user(public_id):
        return UserMaster.query.filter_by(public_id=public_id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
