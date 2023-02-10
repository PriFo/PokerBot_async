from cards import Hand, Cards
from aiogram import types


class Blackjack:

    def __init__(self, user_id: [str, int], msg_4_user: types.Message):
        self.__cards: Cards = Cards()
        self.__user_id: [str, int] = user_id
        self.__user_hand: Hand = Hand()
        self.__bot: BotBlackjack = BotBlackjack()
        self.__message_for_user: types.Message = msg_4_user
        self.__message_for_bot: [types.Message, None] = None
        self.__bet: int = 0

    @property
    def cards(self):
        return self.__cards

    @property
    def user_hand(self):
        return self.__user_hand

    @property
    def user_id(self):
        return self.__user_id

    @property
    def bot(self):
        return self.__bot

    @property
    def bet(self):
        return self.__bet

    @bet.setter
    def bet(self, new_bet):
        self.__bet = new_bet

    @property
    def message_for_user(self):
        return self.__message_for_user

    @property
    def message_for_bot(self):
        return self.__message_for_bot

    @message_for_bot.setter
    def message_for_bot(self, msg_4_bot: types.Message):
        self.__message_for_bot = msg_4_bot


class BotBlackjack:
    """Класс, хранящий руку бота для игры в Blackjack"""

    def __init__(self):
        self.hand: Hand = Hand()
