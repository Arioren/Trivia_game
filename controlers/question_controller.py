from dataclasses import asdict, dataclass
from typing import TypeVar, Optional

from flask import Blueprint, jsonify, request
from toolz import pipe
from toolz.curried import partial

from model.Question import Question
from repository.question_reposiyory import find_all_questions, find_question_by_id, update_question, delete_question
from repository.user_repository import create_question

question_blueprint = Blueprint("trivia_2", __name__)

@question_blueprint.route("/", methods=['GET'])
def find_all():
    questions = list(map(asdict, find_all_questions()))
    return jsonify(questions), 200

@question_blueprint.route("/<int:id>", methods=['GET'])
def find_by_id(id):
    question = pipe(
        find_question_by_id(id),
        partial(map, asdict),
        list
    )
    return jsonify(question), 200

@question_blueprint.route("/create_question", methods=['POST'])
def create_question_from_internet():
    json = request.json
    new_id = create_question(Question(**json))
    return jsonify(new_id), 200


T = TypeVar("T")
@dataclass
class ResponseDto:
    message :Optional[str] = None
    error :Optional[str] = None
    body :Optional[T] = None

@question_blueprint.route("/update_question/<int:id>", methods=['PUT'])
def update_question_from_internet(id:int):
    json = request.json
    question_to_update:Question = next(filter(lambda x: x.id == id, find_all_questions()), None)
    if not question_to_update:
        return jsonify(asdict(ResponseDto(message="question doesnt exists"))), 200

    question_to_update.correct_answer = json["correct_answer"]
    question_to_update.question_text = json["question_text"]
    update_question(question_to_update)

    return jsonify(asdict(ResponseDto(body=question_to_update))), 200

@question_blueprint.route("/delete/<int:id>", methods=['DELETE'])
def delete_question_from_internet(id:int):
    delete_question(id)
    return  jsonify(asdict(ResponseDto(message="user deletes or never existed"))), 200

