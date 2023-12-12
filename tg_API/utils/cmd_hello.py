from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import Command

from database.common.models import *

router = Router()


@router.message(Command("hello_world", "start"))
@router.message(F.text.lower() == "привет")
async def cmd_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!\n"
                         f"Я умею делать API-запросы к ВК и искать там в маркете готовую еду. Начнём? /help")
    data = f"Команда: /hello_world (приветствие)\n"
    try:
        new_request = History(user_id=message.from_user.id, request=data)
        new_request.save()
    except Exception as ex:
        await message.answer(ex.__repr__())
        await message.answer("Что-то пошло не так. Попробуйте ещё раз. Список команд: /help")
