from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
from bot_logging import print_func, print_async_func

load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
DP: Dispatcher = Dispatcher(BOT)


@DP.message_handler(text=["Blackjack"])
@print_async_func()
async def answer_blackjack(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["Правила покера"])
@print_async_func()
async def answer_poker_rules(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["Правила Blackjack"])
@print_async_func()
async def answer_blackjack_rules(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["В главное меню"])
@print_async_func()
async def answer_main_menu(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["Покер"])
@print_async_func()
async def answer_poker(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["Профиль"])
@print_async_func()
async def answer_profile(message: types.Message, **_):
    await message.answer(message.text)


@DP.message_handler(text=["Что умеет бот?"])
@print_async_func()
async def answer_bot_skills(message: types.Message, **_):
    await message.answer(message.text)


@print_func
def start_bot() -> None:
    """
    Function to start bot with printing information of bot into console
    :return: None
    """
    print(f'Start bot...')
    executor.start_polling(DP)
