from functools import partial

import requests
from toolz import pipe


def get_user_by_api():
    url = "https://randomuser.me/api?results=4"
    try:
        response = requests.request("GET", url)
        return pipe(
            response.json(),
            lambda x: x['results'],
            partial(map, lambda x: {'first': x["name"]['first'], 'last': x["name"]['last'], "email": x['email']}),
            list
        )
    except Exception as e:
        print(e)
        return []


def get_question_by_api():
    url = "https://opentdb.com/api.php?amount=20"
    try:
        response = requests.request("GET", url)
        return pipe(
            response.json(),
            lambda x: x['results'],
            partial(map, lambda x: {'question_text': x['question'], 'correct_answer': x['correct_answer'], "incorrect_answers":x["incorrect_answers"]}),
            list
        )
    except Exception as e:
        print(e)
        return []

