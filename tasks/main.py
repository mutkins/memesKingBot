import aioschedule
import asyncio
from tasks.inauguration import do_inauguration
from config import INAUGURATION_DAY, INAUGURATION_TIME


async def scheduler():
    # my_code = f'aioschedule.every().{INAUGURATION_DAY}.at("{INAUGURATION_TIME}").do(do_inauguration)'
    # exec(my_code)
    aioschedule.every().sunday.at('21:40').do(do_inauguration)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
