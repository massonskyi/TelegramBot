import requests
from googletrans import Translator

translator = Translator()


def generate_joke(limit: int = 5):
    api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': 'QbutWqaSxwjb8l6Qsmo7Pg==3Pd8miD9fP42OpbG'})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)


def get_joke(json) -> str:
    yield str(f"original:\n {json['joke']}\n"
              f"translated: \n{translator.translate(json['joke'], src='en', dest='ru').text}\n")


def show(limit):
    joke = generate_joke(limit)
    for i in joke:
        for j in get_joke(i):
            print(j)
