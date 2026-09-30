from maxapi.types import MessageCreated
from typing import Dict, Optional
from maxapi.filters import F

from test import mes_test_oper
from utils import GROUP_CHAT_ID, bot, logger, file_path_report, file_path_month
from maxapi import Dispatcher
from function import read_repot_file, get_str_stat, get_str_month, get_str_total

dp = Dispatcher()


@dp.message_created()
async def echo_handler(event: MessageCreated):
    """
    Обработка команды '/send'
    """

    user_text = event.message.body.text

    if user_text == '/send':
        operator_dict, total_dict= read_repot_file(file_path_report, file_path_month)

        str_month = get_str_month()
        str_total_month = get_str_total(total_dict, operator_dict)
        str_stat_operator = get_str_stat(operator_dict)

        await bot.send_message(chat_id=GROUP_CHAT_ID, text=str_month)

        await bot.send_message(chat_id=GROUP_CHAT_ID, text=str_total_month)
        # await bot.send_message(chat_id=GROUP_CHAT_ID, text=mes_test_oper)
        await bot.send_message(chat_id=GROUP_CHAT_ID, text=str_stat_operator)
        await event.message.answer(f"Файлы обработаны. Итоги отправлены в чат")

    else:
        await event.message.answer("Введена неверная команда!")
