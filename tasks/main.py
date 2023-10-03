import aioschedule
import asyncio
from config import TIME_TO_INAUGURATION
from config import DAY_TO_INAUGURATION
from tasks.inauguration import do_inauguration


async def scheduler():
    aioschedule.every().minute.do(do_inauguration)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
