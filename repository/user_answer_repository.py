from datetime import timedelta

from model.UserAnswer import UserAnswer
from repository.database import get_db_connection


def find_all_UserAnswer():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_answer")
            res = cursor.fetchall()
            users = [UserAnswer(**f) for f in res]
            return users


def create_UserAnswer(UserAnswer : UserAnswer):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            INSERT INTO user_answer (user_id, question_id, answer_text, is_correct, time_taken)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
        ''', (UserAnswer.user_id, UserAnswer.question_id, UserAnswer.answer_text, UserAnswer.is_correct, UserAnswer.time_taken))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id

def load_UserAnswer():
    all_UserAnswer = find_all_UserAnswer()
    if all_UserAnswer and len(all_UserAnswer) > 0:
        return
    create_UserAnswer(UserAnswer(user_id = 1, question_id=1, answer_text="Brazil", is_correct=True, time_taken=timedelta(seconds=42)))
    create_UserAnswer(UserAnswer(user_id=3, question_id=3, answer_text="Mount Everest", is_correct=False,
                                 time_taken=timedelta(seconds=50)))

    create_UserAnswer(UserAnswer(user_id=4, question_id=4, answer_text="Pacific Ocean", is_correct=True,
                                 time_taken=timedelta(seconds=25)))

    create_UserAnswer(UserAnswer(user_id=1, question_id=5, answer_text="Shakespeare", is_correct=False,
                                 time_taken=timedelta(seconds=33)))

    create_UserAnswer(UserAnswer(user_id=2, question_id=6, answer_text="Amazon Rainforest", is_correct=True,
                                 time_taken=timedelta(seconds=28)))

    create_UserAnswer(UserAnswer(user_id=3, question_id=7, answer_text="Albert Einstein", is_correct=True,
                                 time_taken=timedelta(seconds=41)))

    create_UserAnswer(UserAnswer(user_id=4, question_id=8, answer_text="Nile River", is_correct=False,
                                 time_taken=timedelta(seconds=38)))

    create_UserAnswer(
        UserAnswer(user_id=1, question_id=9, answer_text="Mercury", is_correct=True, time_taken=timedelta(seconds=22)))

    create_UserAnswer(UserAnswer(user_id=2, question_id=10, answer_text="Great Wall of China", is_correct=False,
                                 time_taken=timedelta(seconds=45)))