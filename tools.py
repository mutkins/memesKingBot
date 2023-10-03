from aiogram import types


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
