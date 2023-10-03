from aiogram import Dispatcher
from handlers.main_handler import collect_msgs, set_like


def register_all_handlers(dp: Dispatcher):
    dp.register_message_handler(collect_msgs, content_types=['photo', 'document', 'animation', 'video'])
    dp.register_callback_query_handler(set_like, lambda callback: callback.data.startswith('like'))