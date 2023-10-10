import os
import logging
from aiogram import types


# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


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

