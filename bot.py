from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from random import randint

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from blackjack import Blackjack
from bot_logging import print_func, print_async_func, LogDB
from user import Profile, BLACKJACK_WIN_EXP_BOOST, BLACKJACK_GAME_EXP_BOOST, LVL_BONUS
import strings
import markups


GOOD_EMOJI: list = ['😃', '☺️', '🙂', '🥳', '🤩', '😼', '']
BAD_EMOJI: list = ['😞', '😕', '😔', '🙁', '😓', '🫡', '😢', '']
PROFILES: dict = {}
PROFILES_MESSAGES: dict = {}
DB: LogDB = LogDB()
BLACKJACK_OFFLINE: dict = {}
POKER_MESSAGES: dict = {}
load_dotenv('config.env')
API_TOKEN: str = getenv('TOKEN')
BOT: Bot = Bot(token=API_TOKEN)
STORAGE: MemoryStorage = MemoryStorage()
DP: Dispatcher = Dispatcher(BOT, storage=STORAGE)


class BlackjackForm(StatesGroup):
    bet = State()


class ProfileForm(StatesGroup):
    username = State()


@print_async_func()
async def check_lvl(profile: Profile):
    if profile.check_exp():
        await BOT.send_message(
            chat_id=profile.user_id,
            text=f'УРА! {GOOD_EMOJI[randint(0, 6)]} У вас новый уровень!\n'
                 f'Ваш уровень: {profile.level}\nВам на счёт зачислено: {LVL_BONUS}'
        )


@print_async_func()
async def get_profile_text(cur_profile: Profile) -> str:
    return f'Здравствуйте, {cur_profile.username}\n' \
           f'Ваш уровень: {cur_profile.level}\n' \
           f'Ваши средства: {cur_profile.money} у.е.\n\n' \
           f'Что пожелаете?'


@print_async_func()
async def provide_result(game: Blackjack, result: int) -> None:
    profile: Profile = PROFILES.get(str(game.user_id))
    profile.count_blackjack += 1
    if game.message_for_user.reply_markup is not None:
        await game.message_for_user.delete_reply_markup()
    if result in [1, 2, 4, 3]:
        profile.exp += BLACKJACK_WIN_EXP_BOOST
        profile.money += game.bet
        profile.wins_blackjack += 1
        await check_lvl(profile)
        if result == 3:
            await BOT.send_message(
                chat_id=game.user_id,
                text=f"ЗОЛОТОЕ ОЧКО!{GOOD_EMOJI[randint(0, 6)]}"
                     f"\nВам начислено: {game.bet} у.е. и {BLACKJACK_WIN_EXP_BOOST} опыта",
                reply_markup=markups.MAIN_MARKUP
            )
        else:
            await BOT.send_message(
                chat_id=game.user_id,
                text=f"Победа!{GOOD_EMOJI[randint(0, 6)]}"
                     f"\nВам начислено: {game.bet} у.е. и {BLACKJACK_WIN_EXP_BOOST} опыта",
                reply_markup=markups.MAIN_MARKUP
            )
    elif result in [5, 6, 7, 8, 9]:
        profile.exp += BLACKJACK_GAME_EXP_BOOST
        profile.money -= game.bet
        await check_lvl(profile)
        if result == 8:
            await BOT.send_message(
                chat_id=game.user_id,
                text=f'Поражение с золотым очком у дилера...{BAD_EMOJI[randint(0, 7)]}'
                     f'\nВам начислено {BLACKJACK_GAME_EXP_BOOST} опыта',
                reply_markup=markups.MAIN_MARKUP
            )
        elif result == 9:
            await BOT.send_message(
                chat_id=game.user_id,
                text=f'Ничья.{BAD_EMOJI[randint(0, 7)]}'
                     f'\nВам начислено {BLACKJACK_GAME_EXP_BOOST} опыта',
                reply_markup=markups.MAIN_MARKUP
            )
        else:
            await BOT.send_message(
                chat_id=game.user_id,
                text=f'Поражение...{BAD_EMOJI[randint(0, 7)]}\nВам начислено {BLACKJACK_GAME_EXP_BOOST} опыта',
                reply_markup=markups.MAIN_MARKUP
            )
    profile.save_profile_info()


@print_async_func()
async def provide_take_card_user(game: Blackjack) -> None:
    game.add_user_card()
    game.message_for_user = await game.message_for_user.edit_text(
        text=await get_blackjack_offline_user_text(game),
        reply_markup=markups.BLACKJACK_OFFLINE_MARKUP
    )


@print_async_func()
async def provide_take_card_bot(game: Blackjack) -> None:
    game.add_bot_card()
    if game.message_for_bot:
        game.message_for_bot = await game.message_for_bot.edit_text(
            text=await get_blackjack_offline_bot_text(game)
        )
    else:
        game.message_for_bot = await BOT.send_message(
            chat_id=str(game.user_id),
            text=await get_blackjack_offline_bot_text(game)
        )


@print_async_func()
async def get_blackjack_offline_bot_text(game: Blackjack) -> str:
    return f'Карты дилера: {game.bot.hand.get_str_cards()}\n' \
           f'Сумма ваших карт: {game.bot.hand.get_summary()}'


@print_async_func()
async def get_blackjack_offline_user_text(game: Blackjack) -> str:
    return f'Ваши карты: {game.user_hand.get_str_cards()}\n' \
           f'Сумма ваших карт: {game.user_hand.get_summary()}'


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
    exp_4_previous_lvl = profile.get_exp_on_previous_level()
    exp_4_next_lvl = profile.get_exp_for_next_level()
    if profile:
        await query.answer(
            text='Сбор информации...'
        )
        exp: str = str(
            ["█" if int(
                (profile.exp - exp_4_previous_lvl) / ((exp_4_next_lvl - exp_4_previous_lvl) / 16)
            ) > i else "░" for i in range(0, 16)]
        ).replace("\'", "").replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
        text: str = f'Здравствуйте, {profile.username}\n' \
                    f'Ваш уровень: {profile.level}\n' \
                    f'========={profile.exp}/{exp_4_next_lvl}=========\n' \
                    f'{exp}\n\n' \
                    f'Всего покер сессий: {profile.count_poker}\n' \
                    f'Всего побед в покер: {profile.wins_poker}\n\n' \
                    f'Всего Blackjack сессий: {profile.count_blackjack}\n' \
                    f'Всего побед в Blackjack: {profile.wins_blackjack}'
        if msg_4_user.text != text:
            await msg_4_user.edit_text(
                text=text,
                reply_markup=markups.PROFILE_MENU_MARKUP
            )
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
async def process_bet_blackjack_invalid(message: types.Message, **_):
    await message.reply(
        text='Ставка должна быть числом...\n'
             'Введите свою ставку(только цифры)\n'
             'Для отмены нажмите /cancel'
    )


@DP.message_handler(lambda message: message.text.isdigit(), state=BlackjackForm.bet)
@print_async_func()
async def process_bet_blackjack_valid(message: types.Message, state: FSMContext, **_):
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
async def start_blackjack(query: types.CallbackQuery, **_) -> None:
    await query.answer(text='OK!')
    game: Blackjack = BLACKJACK_OFFLINE.get(str(query.from_user.id))
    await provide_take_card_user(game)
    await provide_take_card_bot(game)


@DP.callback_query_handler(text='blackjack_offline_take_card')
@print_async_func()
async def take_card_offline(query: types.CallbackQuery, **_) -> None:
    await query.answer('OK!')
    game: Blackjack = BLACKJACK_OFFLINE.get(str(query.from_user.id))
    await provide_take_card_user(game)
    result: int = game.check_results()
    if result > 0:
        await provide_result(BLACKJACK_OFFLINE.pop(str(query.from_user.id)), result)
    else:
        if game.bot.check_chance(game.cards):
            await provide_take_card_bot(game)
        result = game.check_results()
        if game.check_results() > 0:
            await provide_result(BLACKJACK_OFFLINE.pop(str(query.from_user.id)), result)


@DP.callback_query_handler(text='blackjack_offline_hold')
@print_async_func()
async def hold_offline(query: types.CallbackQuery, **_) -> None:
    await query.answer('OK!')
    game: Blackjack = BLACKJACK_OFFLINE.pop(str(query.from_user.id))
    game.message_for_user = await game.message_for_user.delete_reply_markup()
    while game.bot.check_chance(game.cards):
        await provide_take_card_bot(game)
    result: int = game.check_results(hold=True)
    await provide_result(game, result)


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


@DP.callback_query_handler(text='create_poker_game')
@print_async_func()
async def create_poker_game(query: types.CallbackQuery, **_):
    ...


@DP.callback_query_handler(text='show_poker_games')
@print_async_func()
async def show_poker_games(query: types.CallbackQuery, **_):
    ...


@DP.callback_query_handler(text='exit_poker_menu')
@print_async_func()
async def exit_poker_menu(query: types.CallbackQuery, **_):
    try:
        msg: types.Message = POKER_MESSAGES.pop(str(query.from_user.id))
        await query.answer('OK')
        await msg.edit_text(text='Меню закрыто', reply_markup=None)
    except KeyError as _:
        await query.answer(text="Don't try to use old message keyboard")
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
        await msg_4_user.delete_reply_markup()
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
    await query.answer('OK!')
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
async def answer_start_command(message: types.Message, **_):
    user_info: [dict, None] = DB.get_user_value(str(message.from_user.id))
    if user_info is None:
        DB.input_user_value(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            user_lastname=message.from_user.last_name,
            user_username=message.from_user.username
        )
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
    elif PROFILES.get(str(message.from_user.id)).money < 10:
        await message.answer(
            text='У вас недостаточно средств для начала игры...\n'
                 'Для начала игры требуется 10 у.е.',
            reply_markup=markups.MAIN_MARKUP
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
    POKER_MESSAGES[str(message.from_user.id)] = await message.answer(
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
    profile: [Profile, None] = PROFILES.get(str(message.from_user.id))
    if profile is None:
        PROFILES[str(message.from_user.id)] = Profile(str(message.from_user.id))
    else:
        profile.update_profile_info()
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
