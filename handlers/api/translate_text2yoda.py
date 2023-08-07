import requests


def yoda_translate_text(text) -> str:
    txt = requests.post(url='https://api.funtranslations.com/translate/yoda.json', json={'text': text})
    return txt.json()['contents']['translated']