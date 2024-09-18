from flask import Flask

from controlers.question_controller import question_blueprint
from controlers.user_controller import fighter_blueprint
from repository.database import create_table
from repository.user_answer_repository import load_UserAnswer
from repository.user_repository import load_user_from_api, load_question_answer_api

app = Flask(__name__)

if __name__ == '__main__':
    create_table()
    load_user_from_api()
    load_question_answer_api()
    load_UserAnswer()
    app.register_blueprint(fighter_blueprint, url_prefix="/api/user")
    app.register_blueprint(question_blueprint, url_prefix="/api/question")
    app.run(debug=True)