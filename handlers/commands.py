import logging
from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.types import URLInputFile, FSInputFile

from .utils import *
from settings.api import NASA_API

logging.basicConfig(
    level=logging.DEBUG,
    filename='logging/app.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

router = Router()


@router.message(Command("random_prompt"))
async def _ai_callback_query_generate_prompt(msg: types.Message) -> None:
    text = msg.text[15:]
    output = ai_renerate_prompt(text)
    for i in output:
        await msg.answer(i)


@router.message(Command("check_server"))
async def _ai_callback_query_check_server(msg: types.Message) -> None:
    is_run = check_server()
    if is_run:
        await msg.answer(f"ai server image return {is_run[0]}, ai server prompt return {is_run[1]}")
    else:
        await msg.answer(f"Сервера выключены или на них произошли ошибки")


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
