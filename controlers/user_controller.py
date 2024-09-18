from dataclasses import asdict, dataclass
from typing import TypeVar, Optional

from flask import Blueprint, jsonify, request
from toolz import pipe
from toolz.curried import partial

from model.User import User
from repository.user_repository import find_all_users, create_user, fin_user_by_id, update_user, delete_user

fighter_blueprint = Blueprint("trivia", __name__)

@fighter_blueprint.route("/", methods=['GET'])
def findAll():
    users = list(map(asdict, find_all_users()))
    return jsonify(users), 200

@fighter_blueprint.route("/<int:user_id>", methods=['GET'])
def findById(user_id):
    users = pipe(
        fin_user_by_id(user_id),
        partial(map, asdict),
        list
    )
    return jsonify(users), 200

@fighter_blueprint.route("/create_user", methods=['POST'])
def create_user_from_internet():
    json = request.json
    new_id = create_user(User(**json))
    return jsonify(new_id), 200


T = TypeVar("T")
@dataclass
class ResponseDto:
    message :Optional[str] = None
    error :Optional[str] = None
    body :Optional[T] = None

@fighter_blueprint.route("/update_user/<int:id>", methods=['PUT'])
def update_user_from_internet(id:int):
    json = request.json
    user_to_update:User = next(filter(lambda x: x.id == id, find_all_users()), None)
    if not user_to_update:
        return jsonify(asdict(ResponseDto(message="user doesnt exists"))), 200

    user_to_update.first = json["first"]
    user_to_update.last = json["last"]
    user_to_update.email = json["email"]
    update_user(user_to_update)

    return jsonify(asdict(ResponseDto(body=user_to_update))), 200

@fighter_blueprint.route("/delete/<int:id>", methods=['DELETE'])
def delete_user_from_internet(id:int):
    delete_user(id)
    return  jsonify(asdict(ResponseDto(message="user deletes or never existed"))), 200

