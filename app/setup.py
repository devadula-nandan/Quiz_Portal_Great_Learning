import csv
import uuid
from datetime import datetime

from app.models import QuestionMaster
from app import db

"""
Helper function which will create questions based on the data in questions.csv file
"""


def add_questions():
    try:
        with open('questions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = row['Question']
                choice1 = row['Choice1']
                choice2 = row['Choice2']
                choice3 = row['Choice3']
                choice4 = row['Choice4']
                answer = row['Answer']
                marks = row['Marks']
                remarks = row['Remarks']

                question = QuestionMaster(
                    str(uuid.uuid4()),
                    question,
                    choice1,
                    choice2,
                    choice3,
                    choice4,
                    answer,
                    marks,
                    remarks,
                    True,
                    datetime.utcnow(),
                    datetime.utcnow()
                )

                db.session.add(question)

            db.session.commit()
    except Exception as e:
        print(str(e))
