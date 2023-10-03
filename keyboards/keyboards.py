from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from db.messages import get_msg_from_db_by_id


def get_likes_kb(db_msg_id):

    db_msg = get_msg_from_db_by_id(id=db_msg_id)
    count_of_likes = db_msg.count_of_likes

    if count_of_likes > 0:
        smiles = []
        for i in range(0, count_of_likes):
            smiles.append('😁')
        text = ' '.join(smiles)
    else:
        text = 'Like it!'

    ikb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=text, callback_data=f'like {db_msg_id}')
    ikb.add(button)
    return ikb
