from aiogram.utils import executor
from create_bot import dp
from handlers import register_all_handlers
import asyncio
from tasks import scheduler
from db.db_init import engine, Base


register_all_handlers(dp)
Base.metadata.create_all(engine)


async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
