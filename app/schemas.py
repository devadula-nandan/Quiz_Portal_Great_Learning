from marshmallow import Schema, fields, base


"""
This module aims at providing the request and response format for the various api calls.
This also helpful for creating swagger docs for apis testing.
"""

class APIResponse(Schema):
    message = fields.Str(default="Success")

class SignUpRequest(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()

class LoginRequest(Schema):
    username = fields.Str()
    password = fields.Str()

class AddQuestionsRequest(Schema):
    question = fields.Str()
    choice1 = fields.Str()
    choice2 = fields.Str()
    choice3 = fields.Str()
    choice4 = fields.Str()
    answer = fields.Int()
    marks = fields.Int()
    remarks = fields.Str()

