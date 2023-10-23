from aiogram import Dispatcher, types
from handlers.main_handler import collect_msgs, set_like, collect_albums
from handlers.admin_actions import get_log, get_db


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(collect_albums, is_media_group=True, content_types=['photo', 'document', 'video'])
    dp.register_message_handler(get_log, state='*', commands=['log'])
    dp.register_message_handler(get_db, state='*', commands=['db'])
    dp.register_message_handler(collect_msgs, content_types=['photo', 'document', 'animation', 'video'])
    dp.register_callback_query_handler(set_like, lambda callback: callback.data.startswith('like'))

