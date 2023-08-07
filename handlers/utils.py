import json
import io
import base64
import requests

from googletrans import Translator
from PIL.Image import Image
from aiogram.utils.markdown import text as txt
from module.nasa import Nasa
from PIL import Image, PngImagePlugin
from module.ai.MagicPrompt.MagicPrompt import *
from .api import *


def help() -> txt:
    return txt(
        "Доступные команды:",
        "/help - Помощь",
        "/check_server - проверить состояние сервера",
        "/password {min}{max}- генерация пароля, {} - не обязательный параметр",
        "/image prompt - сгенерировать картинку с помощью ИИ",
        "/random_prompt start prompt - генерация prompt`a по вашему заголовку",
        "/ID - узнать свой id",
        "/nasa_day_photo - получить фото дня из NASA",
        "/evil_insult - сгенерировать случайное оскорбление",
        "/yoda prompt- йода озвучит ваш prompt по-своему",
        "/world time city - узнать мировое время в city",
        "/weather now city- узнать погоду в city",
        "/sentiment prompt- определить интонацию вашего prompt`a",
        "/memes - получить мемес",
        "/fact limit - получить limit случайных фактов",
        "/joke limit - получить limit случайных шуток",
        "/recept prompt - получить рецепты на основе prompt`a",
        sep="\n"
    )


def ai_generate_password(params) -> json:
    url = 'http://127.0.0.1:8001/generate?'
    response = requests.post(url, json=params)
    return response.json()


def ai_generate_prompt(prompt="red people with cap", temperature=1, top_k=12, min_length=20, max_length=90,
                       repetition_penalty=1, num_return_sequences=5) -> json:
    texts = generate("FredZhang7", prompt, temperature, top_k, min_length, max_length, repetition_penalty,
                     num_return_sequences)
    return texts


def ai_generate_image(url, payload) -> None:
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('assets/img/generated/output.png', pnginfo=pnginfo)


def check_server():
    try:
        list_code = []
        page_ai_generate_image = requests.get("http://127.0.0.1:7860")
        page_ai_generate_prompt = requests.get("http://127.0.0.1:8090")
        page_generate_password = requests.get("http://127.0.0.1:8001")
        list_code.append(page_ai_generate_image.status_code)
        list_code.append(page_ai_generate_prompt.status_code)
        list_code.append(page_generate_password.status_code)
        return list_code
    except Exception as e:
        return False


def get_photo_day_from_nasa(nasa_api: str) -> str:
    nasa = Nasa(key=nasa_api)
    url = nasa.picture_of_the_day()['hdurl']
    # import urllib.request
    # urllib.request.urlretrieve(url, "assets/img/nasa/local-filename.jpg")
    # image = Image.open('assets/img/nasa/local-filename.jpg')
    return url


def get_random_evil_insult_generator() -> str:
    url = 'https://evilinsult.com/generate_insult.php?lang=en&type=json'
    response = requests.post(url)
    text = response.json()['insult']
    translator = Translator()
    translation = translator.translate(text, src="en", dest="ru")
    reply = txt(
        f"Original text:",
        f"{text}"
        f"Translated text:",
        f"{translation.text}",
        sep="\n"
    )
    return reply
