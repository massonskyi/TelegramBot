import random

import requests


def get_memes():
    obj = requests.get('https://api.imgflip.com/get_memes')
    """
    with open('pic1.jpg', 'wb') as handle:
        response = requests.get(img_obj.json()['data']['memes'][5]['url'], stream=True)
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)
     """
    return obj.json()['data']['memes'][random.randint(0, len(obj.json()['data']['memes']))]['url']
