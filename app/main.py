from flask import Flask
from flask_restful import Api

from api.generate_answer.generate_answer import GenerateAnswer

app = Flask(__name__)
api = Api(app)

api.add_resource(GenerateAnswer, "/generate-answer/")


def create_app():
    return app
