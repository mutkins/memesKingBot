from aiogram import types
from create_bot import bot
from db.messages import add_msg_to_db, like_db_message, get_msg_from_db_by_id
from db.users import add_user_to_db, get_user_from_db_by_chat_id
from db.likes import add_like_to_db
from keyboards.keyboards import get_likes_kb
from sqlalchemy.exc import IntegrityError
from tools import extract_file_id


async def collect_msgs(message: types.Message):
    user = get_user_from_db_by_chat_id(chat_id=message.from_user.id)
    if not user:
        add_user_to_db(chat_id=message.from_user.id, username=message.from_user.username,
                       first_name=message.from_user.first_name, last_name=message.from_user.last_name,
                       mention=message.from_user.mention)
    file_id = extract_file_id(message)
    db_msg_id = add_msg_to_db(message_id=message.message_id, from_chat_id=message.from_user.id, date=message.date,
                              chat_id=message.chat.id, content_type=message.content_type, file_id=file_id)

    if message.caption:
        caption = message.html_text
    else:
        caption = None
    match message.content_type:
        case 'photo':
            await message.answer_photo(photo=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'video':
            await message.answer_video(video=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'animation':
            await message.answer_animation(animation=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'document':
            await message.answer_document(document=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
    await message.delete()


async def set_like(call: types.CallbackQuery):
    user = get_user_from_db_by_chat_id(chat_id=call.from_user.id)
    if not user:
        add_user_to_db(chat_id=call.from_user.id, username=call.from_user.username, first_name=call.from_user.first_name, last_name=call.from_user.last_name, mention=call.from_user.mention)
    db_msg_id = call.data.split(' ')[1]
    try:
        add_like_to_db(msg_id=db_msg_id, from_user_chat_id=call.from_user.id)
        like_db_message(msg_id=db_msg_id)
    except IntegrityError as e:
        if e.code == 'gkpj':
            await call.answer('Вы уже поставили лайк')
            return
    await call.message.edit_reply_markup(reply_markup=get_likes_kb(db_msg_id=db_msg_id))
