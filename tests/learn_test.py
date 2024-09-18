from datetime import timedelta

import pytest
from repository.database import get_db_connection


@pytest.fixture(scope="module")
def setup_database():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            yield cursor

# Exercise 1
# Description: Find the user with the highest score (most correctly answered questions)
def test(setup_database):
   cursor = setup_database
   cursor.execute('''
        SELECT tu.id, tu.first, tu.last, COUNT(ua.id) AS correct_answers
        FROM trivia_user tu
        JOIN user_answer ua ON tu.id = ua.user_id
        WHERE ua.is_correct = TRUE
        GROUP BY tu.id, tu.first, tu.last
        ORDER BY correct_answers DESC
        LIMIT 1
        ''')
   res = cursor.fetchone()["correct_answers"]
   assert res > 0

# Exercise 2
# Description: Find the question that was answered correctly the fastest
def test_2(setup_database):
    cursor = setup_database
    cursor.execute('''
                SELECT question.id, question.question_text, AVG(user_answer.time_taken) AS res
                FROM question
                JOIN user_answer ON question.id = user_answer.question_id
                WHERE user_answer.is_correct = TRUE
                GROUP BY question.id
                ORDER BY res DESC
                LIMIT 1
                ''')
    res = cursor.fetchone()["question_text"]
    assert len(res) > 0

# Exercise 3
# Description: Find the second-place user and their fastest answer time
# def test_3(setup_database):
def test_3(setup_database):
    setup_database.execute('''
                    SELECT question.id, question.question_text, AVG(user_answer.time_taken) AS res
                    FROM question
                    JOIN user_answer ON question.id = user_answer.question_id
                    WHERE user_answer.is_correct = TRUE
                    GROUP BY question.id
                    ORDER BY res DESC
                    LIMIT 2
                    ''')
    res = setup_database.fetchall()[1]["question_text"]
    assert len(res) > 0

# Exercise 4
# Description: Calculate the average time taken to answer each question
def test_4(setup_database):
    setup_database.execute(
        '''
            SELECT AVG(user_answer.time_taken) AS res
            FROM question
            JOIN user_answer ON question.id = user_answer.question_id
        '''
    )
    res:timedelta = setup_database.fetchone()["res"]
    assert res.total_seconds() > 0

# Exercise 5
# Description: Calculate the success rate for each question
def test_5(setup_database):
    setup_database.execute(
        '''
            SELECT 
                question_id,
                COUNT(*) AS total_answers,
                SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END) AS correct_answers,
                (SUM(CASE WHEN is_correct = TRUE THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) AS success_rate
            FROM 
                user_answer
            GROUP BY 
                question_id
            ORDER BY 
                success_rate DESC;
        '''
    )
    res = setup_database.fetchall()["res"]
    assert res.total_seconds() > 0

# Exercise 6
# Description: Find users who have answered all questions


# Exercise 7
# Description: Calculate the median time taken for correct answers vs incorrect answers


# Exercise 8
# Description: Generate a comprehensive report for each user
# containing total_questions, answered_questions
# correct_answers, avg_time, fastest_answer, slowest_answer
# unanswered_questions. Export result to csv.




