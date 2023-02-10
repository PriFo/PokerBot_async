from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
from bot_logging import print_func, print_async_func, LogDB
from user import Profile
import strings
import markups

PROFILES: dict = {}
load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
DP: Dispatcher = Dispatcher(BOT)


@DP.message_handler(commands=['help'])
async def answer_help_command(message: types.Message, **_):
    await message.answer(
        text=strings.ASK_FOR_HELP,
        reply_markup=markups.ASK_HELP_MARKUP
    )


@print_async_func()
async def answer_blackjack(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_poker_rules(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_blackjack_rules(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_main_menu(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_poker(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_profile(message: types.Message, **_):
    await message.answer(message.text)


@print_async_func()
async def answer_bot_skills(message: types.Message, **_):
    await message.answer(
        text=message.text
    )


@print_async_func()
async def answer_nothing(message: types.Message, **_):
    await message.answer('NOTHING')


@DP.message_handler()
@print_async_func()
async def message_handler(message: types.Message, **_):
    profile = PROFILES.get(str(message.from_user.id))
    if profile is None:
        PROFILES[str(message.from_user.id)] = Profile(str(message.from_user.id))
    if 'что умеет бот' in message.text.lower():
        await answer_bot_skills(message)
    elif 'профиль' in message.text.lower():
        await answer_profile(message)
    elif 'правила покера' in message.text.lower():
        await answer_profile(message)
    elif 'правила blackjack' in message.text.lower():
        await answer_profile(message)
    elif 'в главное меню' in message.text.lower():
        await answer_profile(message)
    elif 'покер' in message.text.lower():
        await answer_profile(message)
    elif 'blackjack' in message.text.lower():
        await answer_profile(message)
    else:
        await answer_nothing(message)


@print_func
def start_bot(skip_updates: bool = False) -> None:
    """
    Function to start bot with printing information of bot into console
    :return: None
    """
    print(f'Start bot...')
    executor.start_polling(DP, skip_updates=skip_updates)
