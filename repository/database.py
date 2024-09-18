import psycopg2
from psycopg2.extras import RealDictCursor

from config.sql_config import SQL_URI


def get_db_connection():
    return psycopg2.connect(SQL_URI,cursor_factory=RealDictCursor)

def create_table():
    create_my_table('''
                CREATE TABLE IF NOT EXISTS trivia_user (
                id SERIAL PRIMARY KEY,
                first VARCHAR(100) NOT NULL,
                last VARCHAR(100) NOT NULL,
                email VARCHAR(50) NOT NULL
                )
                ''')

    create_my_table('''
                   CREATE TABLE IF NOT EXISTS question(
                   id SERIAL PRIMARY KEY,
                   correct_answer VARCHAR(255) NOT NULL,
                   question_text VARCHAR(255) NOT NULL
                   )
                   ''')

    create_my_table('''
                CREATE TABLE IF NOT EXISTS answer (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                incorrect_answer VARCHAR(255) NOT NULL,
                FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE
                )
                ''')


    create_my_table('''
                CREATE TABLE IF NOT EXISTS user_answer (
                id SERIAL PRIMARY KEY,
                question_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                answer_text VARCHAR(255) NOT NULL,
                is_correct BOOLEAN,
                time_taken TIME,
                FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES trivia_user(id) ON DELETE CASCADE
                )
                    ''')


def create_my_table(command: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(command)
            connection.commit()