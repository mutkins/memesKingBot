from logger import log
from db.messages import get_id_user_has_the_most_likes, get_all_chat_id, get_the_most_liked_message
from db.users import get_user_from_db_by_chat_id, incr_was_a_king
from create_bot import bot
from tools import extract_user_fullname
from datetime import datetime, timedelta
from config import INAUGURATION_PERIOD
import Exceptions
import asyncio


async def do_inauguration():
    chats = get_all_chat_id()
    for chat_id in chats:
        chat_id = chat_id[0]
        try:
            fullname, sum_of_likes, user_chat_id = await get_king_of_memes(chat_id=chat_id)
            incr_was_a_king(chat_id=user_chat_id)

        except Exception as e:
            log.error(f'CANNOT GET KING OF MEMES, CAUSE: {e}')
            continue
        try:
            await bot.send_message(chat_id=chat_id, text=f'👑👑👑 ВНИМАНИЕ ВНИМАНИЕ ВНИМАНИЕ 👑👑👑\n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                         f'КОРОЛЬ 🤴🤴🤴 МЕМОВ 🤡🤡🤡 НА ЭТОЙ НЕДЕЛЕ 🗓\n'
                                                        f'-------------------------------------------------------------------------------------------\n'
                                                         f'С РЕЗУЛЬТАТОМ В ФАНТАСТИЧЕСКИЕ <b>{sum_of_likes} лайков</b> 👍👍👍 \n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                         f'                                <b>{fullname}!!!!!!</b>\n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                        f'🥳🥳🥳🥳🥳🥳🎉🎉🎉🎉🎉🎉🎂🎂🎂🎂🎂🎂\n', parse_mode='HTML')
            chat = await bot.get_chat(chat_id=chat_id)
            await chat.set_title(f'ЦТ Король мемов {fullname}')
            await asyncio.sleep(60)
            fullname, count_of_likes, new_message_id = await get_the_most_liked_msg(chat_id=chat_id)
            await bot.send_message(chat_id=chat_id, text=f'☝☝☝☝☝☝☝☝ А ТАКЖЕ ☝☝☝☝☝☝☝☝  ️\n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                         f'САМЫЙ СМЕШНОЙ 😂😂😂😂😂😂  ПОСТ НЕДЕЛИ 🗓\n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                         f'НАБРАВШИЙ НЕВЕРОЯТНЫЕ <b>{count_of_likes} лайков</b> 👍👍👍👍👍👍\n'
                                                         f'-------------------------------------------------------------------------------------------\n'
                                                         f'ЗА АВТОРСТВОМ ✍️✍️✍️<b>{fullname}!!!!!!</b>\n'
                                                         , parse_mode='HTML')
            await bot.forward_message(message_id=new_message_id, from_chat_id=chat_id, chat_id=chat_id, disable_notification=True)
        except Exception as e:
            log.error(log.error(f'CANNOT SEND MESSAGE OR RENAME CHAT, CAUSE: {e}. chat_id is {chat_id}'))
            continue


async def get_king_of_memes(chat_id):
    date = datetime.now() - timedelta(days=INAUGURATION_PERIOD)
    res = get_id_user_has_the_most_likes(chat_id=chat_id, date_from=date)
    if not res:
        raise Exceptions.ResultIsEmptyException(message=f'result of get_id_user_has_the_most_likes() is empty. Chat id is {chat_id}')
    user_chat_id = res[0]
    sum_of_likes = res[1]
    user = get_user_from_db_by_chat_id(chat_id=user_chat_id)
    fullname = extract_user_fullname(user)
    return fullname, sum_of_likes, user_chat_id


async def get_the_most_liked_msg(chat_id):
    date = datetime.now() - timedelta(days=INAUGURATION_PERIOD)
    res = get_the_most_liked_message(chat_id=chat_id, date_from=date)
    if not res:
        raise Exceptions.ResultIsEmptyException(message=f'result of get_the_most_liked_msg() is empty. Chat id is {chat_id}')
    user_chat_id = res[0]
    count_of_likes = res[1]
    new_message_id = res[2]
    user = get_user_from_db_by_chat_id(chat_id=user_chat_id)
    fullname = extract_user_fullname(user)
    return fullname, count_of_likes, new_message_id
