import os
from logger import log
from aiogram import types


def check_admin_rights(func):
    async def wrapper(message: types.Message):
        log.info(f'!!!ADMIN ACTION ATTEMPT: {func}, user = {message.from_user.username}')
        if str(message.from_user.id) == str(os.environ.get('my_chat_id')):
            log.info(f'PERMISSION GRANTED')
            await func(message)
        else:
            log.warning(f'PERMISSION DENIED')
    return wrapper


@check_admin_rights
async def get_log(message: types.Message):
    file = types.InputFile('main.log')
    await message.answer_document(file)


@check_admin_rights
async def get_db(message: types.Message):
    file = types.InputFile('db/king_of_memes.db')
    await message.answer_document(file)
