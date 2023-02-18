from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from blackjack import Blackjack
from bot_logging import print_func, print_async_func, LogDB
from user import Profile
import strings
import markups


PROFILES: dict = {}
PROFILES_MESSAGES: dict = {}
DB: LogDB = LogDB()
BLACKJACK_OFFLINE: dict = {}
load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
STORAGE: MemoryStorage = MemoryStorage()
DP: Dispatcher = Dispatcher(BOT, storage=STORAGE)


class BlackjackForm(StatesGroup):
    bet = State()


class ProfileForm(StatesGroup):
    username = State()


async def get_profile_text(cur_profile: Profile) -> str:
    return f'Здравствуйте, {cur_profile.username}\n' \
           f'Ваш уровень: {cur_profile.level}\n' \
           f'Ваши средства: {cur_profile.money} у.е.\n\n' \
           f'Что пожелаете?'


@print_async_func()
async def send_profile_msg(cur_profile: Profile, chat_id: int = None, message: types.Message = None):
    if chat_id is not None:
        PROFILES_MESSAGES[str(chat_id)] = await BOT.send_message(
            chat_id=chat_id,
            text=await get_profile_text(cur_profile),
            reply_markup=markups.PROFILE_MENU_MARKUP
        )
    elif message is not None:
        PROFILES_MESSAGES[str(message.from_user.id)] = await message.answer(
            text=await get_profile_text(cur_profile),
            reply_markup=markups.PROFILE_MENU_MARKUP
        )


@DP.callback_query_handler(text='profile_info')
@print_async_func()
async def profile_info(query: types.CallbackQuery, **_):
    profile: Profile = PROFILES.get(str(query.from_user.id))
    msg_4_user: types.Message = PROFILES_MESSAGES.get(str(query.from_user.id))
    if profile:
        await query.answer(
            text='Сбор информации...'
        )
        exp: str = str(
            ["█" if int(profile.exp / 6.25) > i else "░" for i in range(0, 16)]
        ).replace("\'", "").replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
        text: str = f'Здравствуйте, {profile.username}\n' \
                    f'Ваш уровень: {profile.level}\n' \
                    f'========={profile.exp}/100=========\n' \
                    f'{exp}\n\n' \
                    f'Всего покер сессий: {profile.count_poker}\n' \
                    f'Всего побед в покер: || {profile.wins_poker} ||\n\n' \
                    f'Всего Blackjack сессий: {profile.count_blackjack}\n' \
                    f'Всего побед в Blackjack: || {profile.wins_blackjack} ||'
        if msg_4_user.text != text:
            await msg_4_user.edit_text(
                text=text,
                reply_markup=markups.PROFILE_MENU_MARKUP
            )
        # await BOT.send_message(
        #     chat_id=query.from_user.id,
        #     text=f'Здравствуйте, {profile.username}\n'
        #          f'Ваш уровень: {profile.level}\n'
        #          f'========={profile.exp}/100=========\n'
        #          f'{exp}\n\n'
        #          f'Всего покер сессий: {profile.count_poker}\n'
        #          f'Всего побед в покер: {profile.wins_poker}\n\n'
        #          f'Всего Blackjack сессий: {profile.count_blackjack}\n'
        #          f'Всего побед в Blackjack: {profile.wins_blackjack}',
        #     reply_markup=markups.PROFILE_MENU_MARKUP
        # )
    else:
        await query.answer(
            text='Я не могу выполнить запрос ;('
        )


@DP.message_handler(state=BlackjackForm.bet, commands='cancel')
@DP.message_handler(Text(equals='cancel', ignore_case=True), state=BlackjackForm.bet)
@print_async_func()
async def cancel_handler_bet_blackjack(message: types.Message, state: FSMContext, **_) -> None:
    """
    Allow user to cancel changing bet
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    game: Blackjack = BLACKJACK_OFFLINE.get(str(message.from_user.id))
    game.message_for_user = await message.reply(
        text=f'Ваша ставка: {game.bet} у.е.',
        reply_markup=markups.BLACKJACK_BET_MARKUP
    )


@DP.message_handler(state=ProfileForm.username, commands='cancel')
@DP.message_handler(Text(equals='cancel', ignore_case=True), state=ProfileForm.username)
@print_async_func()
async def cancel_handler_change_profile_name(message: types.Message, state: FSMContext, **_) -> None:
    """
    Allow user to cancel changing bet
    """
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    profile: Profile = PROFILES.get(str(message.from_user.id))
    PROFILES_MESSAGES[str(message.from_user.id)] = await message.reply(
        text=await get_profile_text(profile),
        reply_markup=markups.PROFILE_MENU_MARKUP
    )


@DP.message_handler(lambda message: not message.text.isdigit(), state=BlackjackForm.bet)
@print_async_func()
async def process_bet_invalid(message: types.Message, **_):
    await message.reply(
        text='Ставка должна быть числом...\n'
             'Введите свою ставку(только цифры)\n'
             'Для отмены нажмите /cancel'
    )


@DP.message_handler(lambda message: message.text.isdigit(), state=BlackjackForm.bet)
@print_async_func()
async def process_bet_valid(message: types.Message, state: FSMContext, **_):
    await state.update_data(bet=int(message.text))
    async with state.proxy() as data:
        game: Blackjack = BLACKJACK_OFFLINE.get(str(message.from_user.id))
        game.bet = data.get('bet')
        game.message_for_user = await message.reply(
            text=f'Ваша ставка: {game.bet} у.е.',
            reply_markup=markups.BLACKJACK_BET_MARKUP
        )
    await state.finish()


@DP.callback_query_handler(
    text=['blackjack_up', 'blackjack_down', 'blackjack_max', 'blackjack_min', 'blackjack_set']
)
@print_async_func()
async def manage_bet(query: types.CallbackQuery, **_):
    profile: Profile = PROFILES.get(str(query.from_user.id))
    game: Blackjack = BLACKJACK_OFFLINE.get(str(query.from_user.id))
    text: str = ''

    if query.data == 'blackjack_up':
        if profile.money >= game.bet * 2:
            game.raise_bet_x2()
            await query.answer('Successful')
        else:
            text = f'У вас недостаточно средств, чтобы сделать ставку...\n' \
                   f'Ваши средства: {str(profile.money)} \n'

    elif query.data == 'blackjack_down':
        game.lower_bet_x2()

    elif query.data == 'blackjack_max':
        game.bet = profile.money

    elif query.data == 'blackjack_min':
        game.bet = 0

    if query.data == 'blackjack_set':
        await BlackjackForm.bet.set()
        game.message_for_user = await game.message_for_user.edit_text(
            text='Введите свою ставку (только цифры)\n'
                 'Для отмены нажмите /cancel',
            reply_markup=None
        )
    else:
        text += f'Ваша ставка: {str(game.bet)} у.е.'
        if game.message_for_user.text != text:
            game.message_for_user = await game.message_for_user.edit_text(
                text=text,
                reply_markup=markups.BLACKJACK_BET_MARKUP
            )
            await query.answer('Skipped')
        else:
            await query.answer('Not changed')


@DP.callback_query_handler(text='blackjack_start')
@print_async_func()
async def start_blackjack(query: types.CallbackQuery, **_):
    ...


@DP.callback_query_handler(text='blackjack_stop')
@print_async_func()
async def exit_blackjack(query: types.CallbackQuery, **_):
    try:
        game: Blackjack = BLACKJACK_OFFLINE.pop(str(query.from_user.id))
        await game.message_for_user.edit_text(text='Игра закрыта', reply_markup=None)
        await query.answer(text='OK!')
    except KeyError as _:
        await query.answer(text='Don\'t try to use old message keyboard')
    finally:
        await BOT.send_message(
            chat_id=query.from_user.id,
            text=strings.MAIN_MENU,
            reply_markup=markups.MAIN_MARKUP
        )


@DP.callback_query_handler(text='exit_profile')
@print_async_func()
async def exit_profile(query: types.CallbackQuery, **_):
    try:
        msg_4_user: types.Message = PROFILES_MESSAGES.pop(str(query.from_user.id))
        await msg_4_user.edit_reply_markup(None)
        await query.answer('OK!')
    except AttributeError as _:
        await query.answer('Don\'t try to use old message keyboard')
    finally:
        await BOT.send_message(
            chat_id=query.from_user.id,
            text=strings.MAIN_MENU,
            reply_markup=markups.MAIN_MARKUP
        )


@DP.callback_query_handler(text='profile_bonus')
@print_async_func()
async def bonus_profile(query: types.CallbackQuery, **_):
    await query.answer(text='Проверка возможности взять бонус...')
    msg_4_user: types.Message = PROFILES_MESSAGES.get(str(query.from_user.id))
    profile = PROFILES.get(str(query.from_user.id))
    if profile.get_bonus():
        await msg_4_user.edit_text(
            text=await get_profile_text(profile),
            reply_markup=markups.PROFILE_MENU_MARKUP
        )
        DB.update_profile_info(profile.get_dict())
    else:
        time: timedelta = timedelta(hours=12) - (datetime.now() - profile.bonus_date)
        await BOT.send_message(
            chat_id=query.from_user.id,
            text=f'Бонус недавно брали, до следующего бонуса осталось '
                 f'{time.seconds//3600}:{(time.seconds//60)%60}:{time.seconds%3600%60}'
        )


@DP.callback_query_handler(text='change_name')
@print_async_func()
async def change_profile_name(query: types.CallbackQuery, **_):
    await ProfileForm.username.set()
    msg_4_user: types.Message = PROFILES_MESSAGES.pop(str(query.from_user.id))
    await msg_4_user.edit_text(
        text=f'Введите новое имя для профиля\nДля отмены нажмите /cancel',
        reply_markup=None
    )


@DP.message_handler(state=ProfileForm.username)
@print_async_func()
async def process_profile_name(message: types.Message, state: FSMContext, **_):
    await state.update_data(username=message.text)
    async with state.proxy() as data:
        profile: Profile = PROFILES.get(str(message.from_user.id))
        profile.username = data.get('username')
        DB.update_profile_info(profile.get_dict())
        PROFILES_MESSAGES[str(message.from_user.id)] = await message.reply(
            text=await get_profile_text(profile),
            reply_markup=markups.PROFILE_MENU_MARKUP
        )
    await state.finish()


@DP.message_handler(commands=['help'])
@print_async_func()
async def answer_help_command(message: types.Message, **_):
    await message.answer(
        text=strings.ASK_FOR_HELP,
        reply_markup=markups.ASK_HELP_MARKUP
    )


@DP.message_handler(commands=['start'])
@print_async_func()
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
        game: Blackjack = BLACKJACK_OFFLINE.get(str(message.from_user.id))
        game.message_for_user = await message.answer(
            text=f'Ваша ставка: {game.bet} у.е.',
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
