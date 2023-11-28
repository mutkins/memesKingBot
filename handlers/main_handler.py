from aiogram import types
from create_bot import bot
from db.messages import add_msg_to_db, like_db_message, get_msg_from_db_by_id, add_new_message_id
from db.likes import add_like_to_db
from keyboards.keyboards import get_likes_kb
from sqlalchemy.exc import IntegrityError
from tools import extract_file_id, check_user, get_caption
from typing import List
from aiogram_media_group import media_group_handler


async def collect_msgs(message: types.Message):
    await check_user(message=message)
    file_id = extract_file_id(message)
    db_msg_id = add_msg_to_db(message_id=message.message_id, from_chat_id=message.from_user.id, date=message.date,
                              chat_id=message.chat.id, content_type=message.content_type, file_id=file_id)

    caption = await get_caption(message)
    match message.content_type:
        case 'photo':
            new_message = await message.answer_photo(photo=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'video':
            new_message = await message.answer_video(video=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'animation':
            new_message = await message.answer_animation(animation=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
        case 'document':
            new_message = await message.answer_document(document=file_id, caption=caption, reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')
    add_new_message_id(msg_id=db_msg_id, new_message_id=new_message.message_id)
    await message.delete()


async def set_like(call: types.CallbackQuery):
    await check_user(message=call)
    db_msg_id = call.data.split(' ')[1]
    try:
        add_like_to_db(msg_id=db_msg_id, from_user_chat_id=call.from_user.id)
        like_db_message(msg_id=db_msg_id)
    except IntegrityError as e:
        if e.code == 'gkpj':
            await call.answer('Вы уже поставили лайк')
            return
    await call.message.edit_reply_markup(reply_markup=get_likes_kb(db_msg_id=db_msg_id))


@media_group_handler
async def collect_albums(messages: List[types.Message]):
    await check_user(message=messages[0])
    file_id = extract_file_id(messages[0])
    db_msg_id = add_msg_to_db(message_id=messages[0].message_id, from_chat_id=messages[0].from_user.id, date=messages[0].date,
                              chat_id=messages[0].chat.id, content_type=messages[0].content_type, file_id=file_id)
    outputMediaMessage = types.MediaGroup()

    for message in messages:
        file_id = extract_file_id(message)
        caption = await get_caption(message)

        match message.content_type:
            case 'photo':
                outputMediaMessage.attach_photo(photo=file_id, caption=caption, parse_mode='HTML')
            case 'video':
                outputMediaMessage.attach_video(video=file_id, caption=caption, parse_mode='HTML')
            case 'document':
                outputMediaMessage.attach_document(document=file_id, caption=caption, parse_mode='HTML')
        await message.delete()

    new_message = await messages[0].answer_media_group(media=outputMediaMessage)
    add_new_message_id(msg_id=db_msg_id, new_message_id=new_message[0].message_id)
    await messages[0].answer(text='Like it?', reply_markup=get_likes_kb(db_msg_id=db_msg_id), parse_mode='HTML')

