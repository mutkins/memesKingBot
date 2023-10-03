import logging
from db.messages import get_likedest_bd_msg, get_id_user_has_the_most_likes, get_all_chat_id
from db.users import get_user_from_db_by_chat_id
from create_bot import bot
from tools import extract_user_fullname

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def do_inauguration():
    for chat_id in get_all_chat_id():
        chat_id = chat_id[0]
        user = get_id_user_has_the_most_likes(chat_id=chat_id)
        fullname = extract_user_fullname(user)
        chat = await bot.get_chat(chat_id=chat_id)
        await chat.set_title(f'ЦТ Король мемов {fullname}')
        await bot.send_message(text=f'КОРОЛЬ МЕМОВ НА ЭТОЙ НЕДЕЛЕ - {fullname} !!!!!!!!')




        # await bot.send_video(chat_id=db_msg.chat_id, video=db_msg.file_id)




