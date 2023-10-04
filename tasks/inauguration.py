import logging
from db.messages import get_id_user_has_the_most_likes, get_all_chat_id
from db.users import get_user_from_db_by_chat_id, incr_was_a_king
from create_bot import bot
from tools import extract_user_fullname
from datetime import datetime, timedelta
from config import INAUGURATION_PERIOD

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def do_inauguration():
    for chat_id in get_all_chat_id():
        chat_id = chat_id[0]
        date = datetime.now() - timedelta(days=INAUGURATION_PERIOD)
        res = get_id_user_has_the_most_likes(chat_id=chat_id, date_from=date)
        user_chat_id = res[0]
        sum_of_likes = res[1]
        user = get_user_from_db_by_chat_id(chat_id=user_chat_id)
        fullname = extract_user_fullname(user)
        chat = await bot.get_chat(chat_id=chat_id)

        await bot.send_message(chat_id=chat_id, text=f'👑👑👑 ВНИМАНИЕ ВНИМАНИЕ ВНИМАНИЕ 👑👑👑\n'
                                                     f'-------------------------------------------------------------------------------------------\n'
                                                     f'КОРОЛЬ 🤴🤴🤴 МЕМОВ 🤡🤡🤡 НА ЭТОЙ НЕДЕЛЕ 🗓\n'
                                                     f'-------------------------------------------------------------------------------------------\n'
                                                     f'С РЕЗУЛЬТАТОМ В ФАНТАСТИЧЕСКИЕ <b>{sum_of_likes} лайков</b> 👍👍👍 \n'
                                                     f'-------------------------------------------------------------------------------------------\n'
                                                     f'                                           <b>{fullname}!!!!!!</b>\n'
                                                     f'-------------------------------------------------------------------------------------------\n'
                                                     f'🥳🥳🥳🥳🥳🥳🎉🎉🎉🎉🎉🎉🎂🎂🎂🎂🎂🎂\n', parse_mode='HTML')
        await chat.set_title(f'ЦТ Король мемов {fullname}')
        incr_was_a_king(chat_id=user_chat_id)


