import os

SQL_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost/trivia_game_db')
SQLALCHEMY_TRACK_MODIFICATIONS = False