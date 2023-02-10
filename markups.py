from aiogram import types


def __do_ask_help_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Правила покера")
    btn2 = types.KeyboardButton("Правила Blackjack")
    btn3 = types.KeyboardButton("Что умеет бот?")
    btn4 = types.KeyboardButton("В главное меню")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


def __do_leave_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("В главное меню")
    markup.add(btn1)
    return markup


# функция для создания разметки клавиатуры для главного меню
def __do_main_markup() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Покер")
    btn2 = types.KeyboardButton("Blackjack")
    btn3 = types.KeyboardButton("Профиль")
    btn4 = types.KeyboardButton("/help")
    markup.add(btn1, btn2)
    markup.add(btn3)
    markup.add(btn4)
    return markup


# функция для создания разметки клавиатуры сообщения для игры в Blackjack
def __do_blackjack_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Взять карту", callback_data='take_card')
    btn2 = types.InlineKeyboardButton(text="Удержать", callback_data='hold')
    markup.add(btn1, btn2)
    return markup


# функция для создания разметки клавиатуры сообщения для игры в покер
def __do_poker_menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Создать игру", callback_data='create_poker_game')
    btn2 = types.InlineKeyboardButton(text="Игры", callback_data='show_poker_games')
    btn3 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='return_to_menu')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def __do_profile_menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Взять бонус", callback_data='profile_bonus')
    btn2 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='exit_profile')
    btn3 = types.InlineKeyboardButton(text="Сменить имя", callback_data='change_name')
    markup.add(btn1, btn2)
    markup.add(btn3)
    return markup


def __do_blackjack_bet_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Поднять ставку x2", callback_data='blackjack_up')
    btn2 = types.InlineKeyboardButton(text="Понизить ставку x2", callback_data='blackjack_down')
    btn3 = types.InlineKeyboardButton(text="Максимальная ставка", callback_data='blackjack_max')
    btn4 = types.InlineKeyboardButton(text="Минимальная ставка", callback_data='blackjack_min')
    btn5 = types.InlineKeyboardButton(text="Своя ставка", callback_data='blackjack_set')
    btn6 = types.InlineKeyboardButton(text="Начать игру", callback_data='blackjack_start')
    btn7 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='blackjack_stop')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5)
    markup.add(btn6)
    markup.add(btn7)
    return markup


# def __do_poker_list_markup(index: int) -> types.InlineKeyboardMarkup:
#     markup = types.InlineKeyboardMarkup()
#     btn1 = types.InlineKeyboardButton(text=str(active_index[index][1] + 1), callback_data='first_poker')
#     btn2 = types.InlineKeyboardButton(text=str(active_index[index][1] + 2), callback_data='second_poker')
#     btn3 = types.InlineKeyboardButton(text=str(active_index[index][1] + 3), callback_data='third_poker')
#     btn4 = types.InlineKeyboardButton(text=str(active_index[index][1] + 4), callback_data='fourth_poker')
#     btn5 = types.InlineKeyboardButton(text=str(active_index[index][1] + 5), callback_data='fifth_poker')
#     btn6 = types.InlineKeyboardButton(text="Назад", callback_data='back_poker')
#     btn7 = types.InlineKeyboardButton(text="Далее", callback_data='next_poker')
#     btn8 = types.InlineKeyboardButton(text="Закрыть меню", callback_data='return_to_menu')
#     markup.add(btn1, btn2, btn3, btn4, btn5)
#     markup.add(btn6, btn7)
#     markup.add(btn8)
#     return markup


def __do_poker_wait_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Выйти из игры", callback_data='exit_from_poker_game')
    markup.add(btn1)
    return markup


def __do_poker_game_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Поднять', callback_data='raise_bet_poker')
    btn2 = types.InlineKeyboardButton(text='Принять', callback_data='accept_bet_poker')
    btn3 = types.InlineKeyboardButton(text='Пас', callback_data='pass_poker')
    btn4 = types.InlineKeyboardButton(text='All in', callback_data='all_in_poker')
    btn5 = types.InlineKeyboardButton(text="Выйти из игры", callback_data='exit_from_poker_game')
    markup.add(btn1, btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)
    return markup


ASK_HELP_MARKUP: types.ReplyKeyboardMarkup = __do_ask_help_markup()
POKER_GAME_MARKUP: types.InlineKeyboardMarkup = __do_poker_game_markup()
POKER_WAIT_MARKUP: types.InlineKeyboardMarkup = __do_poker_wait_markup()
POKER_MENU_MARKUP: types.InlineKeyboardMarkup = __do_poker_menu_markup()
LEAVE_MARKUP: types.ReplyKeyboardMarkup = __do_leave_markup()
MAIN_MARKUP: types.ReplyKeyboardMarkup = __do_main_markup()
BLACKJACK_BET_MARKUP: types.InlineKeyboardMarkup = __do_blackjack_bet_markup()
BLACKJACK_MARKUP: types.InlineKeyboardMarkup = __do_blackjack_markup()
PROFILE_MENU_MARKUP: types.InlineKeyboardMarkup = __do_profile_menu_markup()

