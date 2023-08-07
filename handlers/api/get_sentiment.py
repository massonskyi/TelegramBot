import requests


def get_sentiment(text):
    api_url = 'https://api.api-ninjas.com/v1/sentiment?text={}'.format(text)
    response = requests.get(api_url, headers={'X-Api-Key': 'QbutWqaSxwjb8l6Qsmo7Pg==3Pd8miD9fP42OpbG'})
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
