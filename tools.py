from aiogram import types
from db.users import Users
from db.users import add_user_to_db, get_user_from_db_by_chat_id


def extract_file_id(message: types.Message):
    match message.content_type:
        case 'photo':
            file_id = message.photo[0].file_id
        case 'video':
            file_id = message.video.file_id
        case 'animation':
            file_id = message.animation.file_id
        case 'document':
            file_id = message.document.file_id
        case _:
            file_id = None
    return file_id


def extract_user_fullname(user: Users):
    fullname = ''
    if user.first_name:
        fullname += user.first_name + ' '
    if user.last_name:
        fullname += user.last_name + ' '
    if user.mention:
        fullname += user.mention
    return fullname


async def check_user(message: types.Message):
    user = get_user_from_db_by_chat_id(chat_id=message.from_user.id)
    if not user:
        add_user_to_db(chat_id=message.from_user.id, username=message.from_user.username,
                       first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                       mention=message.from_user.mention)


async def get_caption(message: types.Message):
    if message.caption:
        caption = message.html_text
    else:
        caption = None
    return caption
