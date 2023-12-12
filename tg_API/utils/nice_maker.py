import aiogram
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest


async def make_it_nice(result: list, message: Message):
    count = 1
    for item in result:
        product = f"<b>#{count}:</b>\n\n" \
                  f"<b><a href='{item.link}'>{item.name}</a></b> \n\n" \
                  f"{item.description} \n\n" \
                  f"<b>Цена</b>: {item.price} {item.currency}"
        if len(product) < 1000:
            await message.bot.send_photo(chat_id=message.chat.id,
                                         photo=item.photo,
                                         caption=product,
                                         parse_mode=ParseMode.HTML)
        else:
            for x in range(0, len(product), 1000):
                await message.bot.send_photo(chat_id=message.chat.id,
                                             photo=item.photo,
                                             caption=product[x:x + 1000],
                                             parse_mode=ParseMode.HTML)

        count += 1
