import logging
import json
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from googletrans import Translator
from .utils import *
from settings.settings_api import NASA_API

logging.basicConfig(
    level=logging.DEBUG,
    filename='logging/app.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

router = Router()


@router.message(Command("yoda"))
async def _ai_callback_query_translate_yoda(msg: types.Message) -> None:
    translator = Translator()
    t = translator.translate(msg.text[len("/yoda"):], src='ru', dest='en')
    res = yoda_translate_text(t.text)
    t = translator.translate(res, src='en', dest='ru')
    await msg.answer(res)
    await msg.answer(t.text)


@router.message(Command("world_time"))
async def _ai_callback_query_world_time(msg: types.Message) -> None:
    res = get_world_time(msg.text[len("/world_time"):])
    await msg.answer(json.dumps(res, indent=2))


@router.message(Command("weather_now"))
async def _ai_callback_query_weather_now(msg: types.Message) -> None:
    res = get_weather_now(msg.text[len("/weather_now"):])
    await msg.answer(res)


@router.message(Command("sentiment"))
async def _ai_callback_query_sentiment(msg: types.Message) -> None:
    sent = get_sentiment(msg.text[10:])
    await msg.answer(sent['sentiment'])


@router.message(Command("memes"))
async def _ai_callback_query_api_memes(msg: types.Message) -> None:
    memes = get_memes()
    await msg.answer_photo(memes)


@router.message(Command("fact"))
async def _ai_callback_query_api_fact(msg: types.Message) -> None:
    text = msg.text[5:]
    res = get_facts(int(text))
    for i in res:
        await msg.answer(json.dumps(i, indent=2))


@router.message(Command("joke"))
async def _ai_callback_query_api_joke(msg: types.Message) -> None:
    text = msg.text[5:]
    res = generate_joke(int(text))
    for i in res:
        for j in get_joke(i):
            await msg.answer(j)


@router.message(Command("recept"))
async def _ai_callback_query_api_recept_cocktail(msg: types.Message) -> None:
    translator = Translator()
    t = translator.translate(msg.text[len('/recept'):], src='ru', dest='en')
    res = get_cocktail(t.text)
    for i in res:
        await msg.answer(json.dumps(i, indent=2))


@router.message(Command("random_prompt"))
async def _ai_callback_query_generate_prompt(msg: types.Message) -> None:
    text = msg.text[15:]
    output = ai_generate_prompt(text)
    for i in output:
        await msg.answer(i)


@router.message(Command("check_server"))
async def _ai_callback_query_check_server(msg: types.Message) -> None:
    is_run = check_server()
    i = 0
    if not is_run:
        for i in is_run:
            if is_run:
                await msg.answer(f"server {'ai' if i == 0 or 1 else 'password_generate'} {is_run[i]}")
            else:
                await msg.answer(
                    f"Сервер {'ai' if i == 0 or 1 else 'password_generate'} выключен или на нем произошла ошибка")
            i += 1
    else:
        await msg.answer("Все сервера в данный момент выключены")


@router.message(Command("password"))
async def _ai_callback_query_password(msg: types.Message) -> None:
    # if not msg.text.find("min") or ("max")
    params = {
        "min": 12,
        "max": 20,
        "only_lower_case": False,
        "used_digits": True,
        "used_punctuation": True,
        "first_number": False
    }
    res = ai_generate_password(params)
    await msg.answer(json.dumps(res, indent=2))


@router.message(Command("start"))
async def _ai_callback_query_start(msg: types.Message) -> None:
    await msg.answer("Привет!\nЧтобы узнать что я могу введите команду /help")


@router.message(Command("ID"))
async def _ai_callback_query_id(msg: types.Message) -> None:
    await msg.answer(f"Ваш id: {msg.from_user.id}")


@router.message(Command("help"))
async def _ai_callback_query_help(message: types.Message) -> None:
    await message.reply(help())


@router.message(Command("nasa_day_photo"))
async def _ai_callback_query_photo_day(msg: types.Message) -> None:
    image = get_photo_day_from_nasa(NASA_API)
    await msg.answer_photo(image)


@router.message(Command("evil_insult"))
async def _ai_callback_query_evil_insult_generator(msg: types.Message) -> None:
    await msg.reply(get_random_evil_insult_generator())


@router.message(Command("image"))
async def _ai_callback_query_image_gen(msg: types.Message) -> None:
    text = msg.text[6:]
    payload = {
        "prompt": f"{text}",
        "sampler_index": "DDIM",
        "steps": 50,
        "negative_prompt": None,
    }
    ai_generate_image("http://127.0.0.1:7860", payload)
    image = FSInputFile('assets/img/generated/output.png', 'rb')
    await msg.answer_photo(image)
