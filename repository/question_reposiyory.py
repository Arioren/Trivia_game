from toolz import pipe
from toolz.curried import partial

from model.Question import Question
from repository.database import get_db_connection


def find_all_questions():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM question")
            res = cursor.fetchall()
            users = [Question(**f) for f in res]
            return users

def find_question_by_id(id):
    return pipe(
        find_all_questions(),
        partial(filter, lambda x: x.id == id),
        list
    )

def update_question(question : Question):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            UPDATE question
            SET question_text = %s , correct_answer = %s
            WHERE id = %s
                            ''',(question.question_text, question.correct_answer, question.id))
            connection.commit()

def delete_question(id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM question WHERE id = %s; ''', (id,))
            connection.commit()
