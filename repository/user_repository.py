from typing import List

from toolz import pipe, first
from toolz.curried import partial

from api.user_question_api import get_user_by_api, get_question_by_api
from model.Answer import Answer
from model.Question import Question
from model.User import User
from model.UserAnswer import UserAnswer
from repository.database import get_db_connection


def load_user_from_api():
    all_users = find_all_users()
    if all_users and len(all_users) > 0:
        return
    users_json = get_user_by_api()
    for f in [User(**f) for f in users_json]:
        create_user(f)

def load_question_answer_api():
    all_question = find_all_question()
    if all_question and len(all_question) > 0:
        return
    question_json = get_question_by_api()
    for f in question_json:
        new_id = create_question(Question(question_text=f["question_text"], correct_answer=f["correct_answer"]))
        for q in f["incorrect_answers"]:
            create_answer(Answer(question_id=new_id, incorrect_answer=q))

def create_user(user: User) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO trivia_user (first, last, email)
                VALUES (%s, %s, %s) RETURNING id
            """, (user.first, user.last, user.email))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id

def create_answer(answer: Answer) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO answer (incorrect_answer, question_id)
                VALUES (%s, %s) RETURNING id
            """, (answer.incorrect_answer, answer.question_id))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id

def create_question(question: Question) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO question (question_text, correct_answer)
                VALUES (%s, %s) RETURNING id
            """, (question.question_text , question.correct_answer))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id


def find_all_users()->List[User]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM trivia_user")
            res = cursor.fetchall()
            users = [User(**f) for f in res]
            return users


def fin_user_by_id(int_id):
    return pipe(
        find_all_users(),
        partial(filter, lambda x:x.id == int_id),
        list
    )

def find_all_question():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM question")
            res = cursor.fetchall()
            question = [Question(**f) for f in res]
            return question

def update_user(user:User):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            UPDATE trivia_user
            SET first = %s , last= %s, email = %s
            WHERE id = %s
                            ''',(user.first, user.last, user.email, user.id))
            connection.commit()


def delete_user(id:int):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM trivia_user WHERE id = %s; ''',(id,))
            connection.commit()
