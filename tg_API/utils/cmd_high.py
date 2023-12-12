import peewee
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.common.models import *
from site_API.core import vk_api, url, params
from tg_API.utils import nice_maker


class HighStates(StatesGroup):
    input_food = State()
    input_count = State()


router = Router()


@router.message(Command("high"))
async def cmd_low(message: Message, state: FSMContext):
    await state.update_data(created_at=datetime.now())
    await message.answer("Напишите, какую еду вам показать: ")
    await state.set_state(HighStates.input_food)


@router.message(StateFilter(HighStates.input_food), F.text.isalpha())
async def food_sent(message: Message, state: FSMContext):
    params['q'] = message.text
    await message.answer("Напишите, сколько результатов вывести:")
    await state.set_state(HighStates.input_count)


@router.message(StateFilter(HighStates.input_food))
async def warning_not_food(message: Message):
    await message.answer(text="Пожалуйста, напишите корректное наименование еды для поиска: ")


@router.message(StateFilter(HighStates.input_count), F.text.isdigit(), F.text != "0")
async def count_sent(message: Message, state: FSMContext):
    if int(message.text) >= 100:
        await warning_not_count(message)
    else:
        params['count'] = int(message.text)
        result = vk_api.get_high(url=url, params=params)
        if result:
            await nice_maker.make_it_nice(result, message)
            await message.answer("Ваш запрос успешно выполнен. Попробуйте и другие команды: /help")
        else:
            await message.answer("К сожалению, по вашему запросу ничего не найдено. "
                                 "Попробуйте выполнить команду еще раз.")
        data = f"Команда: /high (по убыванию цены)\n" \
               f"Текст запроса: {params['q']} в количестве {params['count']} шт\n"
        try:
            new_request = History(user_id=message.from_user.id, request=data)
            new_request.save()
        except Exception as ex:
            await message.answer(ex.__repr__())
            await message.answer("Что-то пошло не так. Попробуйте ещё раз. Список команд: /help")
        await state.clear()


@router.message(StateFilter(HighStates.input_count))
async def warning_not_count(message: Message):
    await message.answer(text="Пожалуйста, отправьте ЦЕЛОЕ ЧИСЛО больше ноля и не больше 100 "
                              "для выбора количества выводимых результатов:")
