from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from site_API.core import vk_api, url, params
from aiogram.fsm.state import State, StatesGroup

from tg_API.utils import nice_maker
from database.common.models import *


class CustomStates(StatesGroup):
    input_food = State()
    input_count = State()
    input_price_from: State = State()
    input_price_to: State = State()


router = Router()


@router.message(Command("custom"))
async def cmd_low(message: Message, state: FSMContext):
    await message.answer("Напишите, какую еду вам показать: ")
    await state.set_state(CustomStates.input_food)


@router.message(StateFilter(CustomStates.input_food), F.text.isalpha())
async def food_sent(message: Message, state: FSMContext):
    await state.update_data(q=message.text)
    params["q"] = message.text
    await message.answer("Напишите, сколько результатов вывести:")
    await state.set_state(CustomStates.input_count)


@router.message(StateFilter(CustomStates.input_food))
async def warning_not_food(message: Message):
    await message.answer(text="Пожалуйста, напишите корректное наименование еды для поиска: ")


@router.message(StateFilter(CustomStates.input_count), F.text.isdigit(), F.text != "0")
async def count_sent(message: Message, state: FSMContext):
    if int(message.text) > 100:
        await warning_not_count(message)
    else:
        await state.update_data(count=message.text)
        params["count"] = int(message.text)
        await message.answer("Задание ценового диапазона поиска - цена от: ")
        await state.set_state(CustomStates.input_price_from)


@router.message(StateFilter(CustomStates.input_count))
async def warning_not_count(message: Message):
    await message.answer(text="Пожалуйста, отправьте ЦЕЛОЕ ЧИСЛО не меньше ноля и не больше 100 "
                              "для выбора количества выводимых результатов:")


@router.message(StateFilter(CustomStates.input_price_from), F.text.isdigit())
async def count_sent(message: Message, state: FSMContext):
    await state.update_data(price_from=message.text)
    params['price_from'] = int(message.text) * 100
    await message.answer("Задание ценового диапазона поиска - цена до: ")
    await state.set_state(CustomStates.input_price_to)


@router.message(StateFilter(CustomStates.input_price_from))
async def warning_not_price_from(message: Message):
    await message.answer(text="Пожалуйста, отправьте ЦЕЛОЕ ЧИСЛО для задания ценового диапазона:")


@router.message(StateFilter(CustomStates.input_price_to), F.text.isdigit())
async def count_sent(message: Message, state: FSMContext):
    if int(message.text) * 100 >= params["price_from"]:
        await state.update_data(price_to=message.text)
        params['price_to'] = int(message.text) * 100
        result = vk_api.get_custom(url=url, params=params)
        if result:
            await nice_maker.make_it_nice(result, message)
            await message.answer("Ваш запрос успешно выполнен. Попробуйте и другие команды: /help")
        else:
            await message.answer(
                "К сожалению, по вашему запросу ничего не найдено. Попробуйте выполнить команду еще раз.")
        data = f"<b>Команда</b>: /custom (по заданному ценовому диапазону)\n" \
               f"<b>Текст запроса</b>: {params['q']} в количестве {params['count']} шт\n" \
               f"<b>Цена от:</b> {params['price_from'] // 100}\n" \
               f"<b>Цена до:</b> {params['price_to'] // 100}\n"
        try:
            new_request = History(user_id=message.from_user.id, request=data)
            new_request.save()
        except Exception as ex:
            await message.answer(ex.__repr__())
            await message.answer("Что-то пошло не так. Попробуйте ещё раз. Список команд: /help")
        await state.clear()
    else:
        await warning_not_price_to(message)


@router.message(StateFilter(CustomStates.input_price_to))
async def warning_not_price_to(message: Message):
    await message.answer(text="ЦЕНА ДО должна быть меньше ЦЕНЫ ОТ, введите значение ЦЕНЫ ДО:")
