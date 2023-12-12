from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from database.common.models import *

router = Router()


@router.message(Command("help"))
async def cmd_hello(message: Message):
    await message.answer(f"/low - выведет заданное количество выбранной еды по возрастанию цены\n"
                         f"/high - выведет заданное количество выбранной еды по убыванию цены\n"
                         f"/custom - выведет заданное количество выбранной еды "
                         f"в заданном диапазоне цен\n"
                         f"/history - выведет историю запросов")
    data = f"Команда: /help (помощь)\n"
    try:
        new_request = History(user_id=message.from_user.id, request=data)
        new_request.save()
    except Exception as ex:
        await message.answer(ex.__repr__())
        await message.answer("Что-то пошло не так. Попробуйте ещё раз. Список команд: /help")
