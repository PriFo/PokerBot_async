from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv

from blackjack import Blackjack
from bot_logging import print_func, print_async_func, LogDB
from user import Profile
import strings
import markups


PROFILES: dict = {}
DB: LogDB = LogDB()
BLACKJACK_OFFLINE: dict = {}
load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
DP: Dispatcher = Dispatcher(BOT)


async def send_profile_msg(cur_profile: Profile, chat_id: int = None, message: types.Message = None):
    text = f'Здравствуйте, {cur_profile.username}\n' \
           f'Ваш уровень: {cur_profile.level}\n' \
           f'Ваши средства: {cur_profile.money} у.е.\n\n' \
           f'Что пожелаете?'
    if chat_id is not None:
        await BOT.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=markups.PROFILE_MENU_MARKUP
        )
    elif message is not None:
        await message.answer(
            text=text,
            reply_markup=markups.PROFILE_MENU_MARKUP
        )


@print_async_func()
@DP.callback_query_handler(text='profile_info')
async def profile_info(query: types.CallbackQuery):
    profile = PROFILES.get(str(query.from_user.id))
    if profile:
        await query.answer(
            text='Сбор информации...'
        )
        exp: str = str(
            ["=" if profile.exp / 10 > i else "-" for i in range(0, 10)]
        ).replace("\'", "").replace('[', '').replace(']', '').replace(',', '')
        await BOT.send_message(
            chat_id=query.from_user.id,
            text=f'Здравствуйте, {profile.username}\n'
                 f'Ваш уровень: {profile.level}\n'
                 f'........exp.........\n'
                 f'[{exp}]\n\n'
                 f'Всего покер сессий: {profile.count_poker}\n'
                 f'Всего побед в покер: {profile.wins_poker}\n\n'
                 f'Всего Blackjack сессий: {profile.count_blackjack}\n'
                 f'Всего побед в Blackjack: {profile.wins_blackjack}',
            reply_markup=markups.PROFILE_MENU_MARKUP
        )
    else:
        await query.answer(
            text='Я не могу выполнить запрос ;('
        )


@print_async_func()
@DP.callback_query_handler(text='exit_profile')
async def exit_profile(query: types.CallbackQuery):
    await query.answer('OK!')
    await BOT.send_message(
        chat_id=query.from_user.id,
        text=strings.MAIN_MENU,
        reply_markup=markups.MAIN_MARKUP
    )


@print_async_func()
@DP.callback_query_handler(text='profile_bonus')
async def bonus_profile(query: types.CallbackQuery):
    await query.answer(text='Проверка возможности взять бонус...')
    profile = PROFILES.get(str(query.from_user.id))
    if profile.get_bonus():
        await send_profile_msg(cur_profile=profile, chat_id=query.from_user.id)
        DB.update_profile_info(profile.get_dict())
    else:
        time: timedelta = timedelta(hours=12) - (datetime.now() - profile.bonus_date)
        await BOT.send_message(
            chat_id=query.from_user.id,
            text=f'Бонус недавно брали, до следующего бонуса осталось '
                 f'{time.seconds//3600}:{(time.seconds//60)%60}:{time.seconds%3600%60}'
        )
        print(f'now: {datetime.now()}\nbonus_date: {profile.bonus_date}\ntimedelta: {timedelta(hours=12)}')


@print_async_func()
@DP.message_handler(commands=['help'])
async def answer_help_command(message: types.Message, **_):
    await message.answer(
        text=strings.ASK_FOR_HELP,
        reply_markup=markups.ASK_HELP_MARKUP
    )


@print_async_func()
@DP.message_handler(commands=['start'])
async def answer_help_command(message: types.Message, **_):
    await message.answer(
        text=strings.START_TEXT,
        reply_markup=markups.MAIN_MARKUP
    )


@print_async_func()
async def answer_blackjack(message: types.Message, **_):
    await BOT.send_message(
        message.from_user.id,
        text='Предварительная подготовка...',
        reply_markup=markups.REMOVE_MARKUP
    )
    if BLACKJACK_OFFLINE.get(str(message.from_user.id)):
        await message.answer(
            text='Закончите предыдущую игру'
        )
    else:
        BLACKJACK_OFFLINE[str(message.from_user.id)] = Blackjack(message.from_user.id)
        game = BLACKJACK_OFFLINE.get(str(message.from_user.id))
        await message.answer(
            text=f'Ваша ставка: {game.bet}',
            reply_markup=markups.BLACKJACK_BET_MARKUP
        )


@print_async_func()
async def answer_poker_rules(message: types.Message, **_):
    await message.answer(
        text=strings.POKER_RULES,
        reply_markup=markups.LEAVE_MARKUP
    )


@print_async_func()
async def answer_blackjack_rules(message: types.Message, **_):
    await message.answer(
        text=strings.BLACKJACK_RULES,
        reply_markup=markups.LEAVE_MARKUP
    )


@print_async_func()
async def answer_main_menu(message: types.Message, **_):
    await message.answer(
        text=strings.MAIN_MENU,
        reply_markup=markups.MAIN_MARKUP
    )


@print_async_func()
async def answer_poker(message: types.Message, **_):
    await message.answer(
        text='Вы в меню покера\nВыберите действие',
        reply_markup=markups.POKER_MENU_MARKUP
    )


@print_async_func()
async def answer_profile(message: types.Message, **_):
    await BOT.send_message(
        chat_id=int(message.from_user.id),
        text='Предварительная подготовка...',
        reply_markup=markups.REMOVE_MARKUP
    )
    cur_profile = PROFILES.get(str(message.from_user.id))
    await send_profile_msg(cur_profile=cur_profile, message=message)


@print_async_func()
async def answer_bot_skills(message: types.Message, **_):
    await message.answer(
        text=strings.BOT_FUNCTIONS,
        reply_markup=markups.LEAVE_MARKUP
    )


@print_async_func()
async def answer_nothing(message: types.Message, **_):
    await message.answer(
        text='Я вас не понимаю, вы перенаправлены на главное меню',
        reply_markup=markups.MAIN_MARKUP
    )


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
        await answer_poker_rules(message)
    elif 'правила blackjack' in message.text.lower():
        await answer_blackjack_rules(message)
    elif 'в главное меню' in message.text.lower():
        await answer_main_menu(message)
    elif 'покер' in message.text.lower():
        await answer_poker(message)
    elif 'blackjack' in message.text.lower():
        await answer_blackjack(message)
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
