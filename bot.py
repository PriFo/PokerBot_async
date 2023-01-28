from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
from bot_logging import print_func, print_async_func

load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
DP: Dispatcher = Dispatcher(BOT)


@print_async_func()
async def answer_message(message: types.Message):
    ...


@print_async_func()
async def start_bot() -> None:
    """
    Function to start bot with printing information of bot into console
    :return: None
    """
    await DP.start_polling()
