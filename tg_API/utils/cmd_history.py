from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.enums import ParseMode

from database.common.models import *

router = Router()


@router.message(Command("history"))
async def cmd_history(message: Message):
    data = f"Команда: /history (история запросов)\n"
    try:
        new_request = History(user_id=message.from_user.id, request=data)
        new_request.save()
    except Exception as ex:
        await message.answer(ex.__repr__())
        await message.answer("Что-то пошло не так. Попробуйте ещё раз. Список команд: /help")

    user_history = History\
        .select()\
        .where(History.user_id == message.from_user.id)\
        .order_by(History.created_at.desc())
    if user_history:
        await message.answer(text="<b>Ваши последние запросы:</b>", parse_mode='HTML')
        count = 1
        for item in user_history:
            if count <= 10:
                await message.answer(text=f'<b>#{count}</b>:\n'
                                          f'{item.request}\n'
                                          f'<b>Дата</b>: {item.created_at}',
                                     parse_mode=ParseMode.HTML)
                count += 1
    else:
        await message.answer("Ваша история запросов пока пуста. Сделайте свой первый запрос: /help")
