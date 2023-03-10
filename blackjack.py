from cards import Hand, Cards
from aiogram import types


MIN_BET: int = 10


class BotBlackjack:
    """Класс, хранящий руку бота для игры в Blackjack"""

    def __init__(self):
        self.__hand: Hand = Hand()
        self.__go_next: bool = True

    def check_chance(self, cards: Cards) -> bool:
        if self.__go_next:
            summary_bot: int = self.__hand.get_summary()
            need_to_win: int = 21 - summary_bot
            count_of_ok: int = 0
            count_of_all: int = len(cards.cards)
            for i in cards.cards:
                if i.value > 10:
                    if 10 <= need_to_win:
                        count_of_ok += 1
                elif i.value <= need_to_win:
                    count_of_ok += 1
            chance = count_of_ok / count_of_all
            if chance < 0.35:
                self.__go_next = False
                return False
            else:
                return True
        else:
            return self.__go_next

    @property
    def hand(self):
        return self.__hand

    def __hash__(self):
        return hash(self.__hand)


class Blackjack:

    def __init__(self, user_id: [str, int]):
        self.__cards: Cards = Cards()
        self.__user_id: [str, int] = user_id
        self.__user_hand: Hand = Hand()
        self.__bot: BotBlackjack = BotBlackjack()
        self.__message_for_user: [types.Message, None] = None
        self.__message_for_bot: [types.Message, None] = None
        self.__bet: int = 10

    def __hash__(self):
        return hash((
            self.__bet,
            self.__bot,
            self.__message_for_bot,
            self.__message_for_user,
            self.__user_id,
            self.__user_hand,
            self.__cards
        ))

    def check_results(self, hold: bool = False) -> int:
        """
        Проверка результата игры
        :return: 0 - Продолжение игры;
                1 - Победа с суммой карт больше, чем у бота;
                2 - Победа с суммой карт 21;
                3 - Победа с 2мя тузами;
                4 - Победа, у бота больше 21;
                5 - Поражение с суммой карт меньше, чем у бота;
                6 - Поражение с суммой карт больше 21;
                7 - Поражение, бот с суммой карт 21;
                8 - Поражение, бот с 2мя тузами;
                9 - Ничья
        """
        if self.__get_user_21():
            return 2
        elif self.__get_bot_21():
            return 7
        elif self.__get_user_ace_win():
            return 3
        elif self.__get_bot_ace_win():
            return 8
        elif self.__get_user_lose():
            return 6
        elif self.__get_bot_lose():
            return 4
        elif hold and not self.__bot.check_chance(self.__cards):
            if self.__get_draw():
                return 9
            elif self.__get_user_win():
                return 1
            else:
                return 5
        else:
            return 0

    def add_user_card(self) -> None:
        self.__user_hand.add_card(self.__cards.get_card())

    def add_bot_card(self) -> None:
        self.__bot.hand.add_card(self.__cards.get_card())

    def raise_bet_x2(self) -> None:
        self.__bet *= 2

    def lower_bet_x2(self) -> None:
        if self.__bet // 2 <= MIN_BET:
            self.__bet = MIN_BET
        else:
            self.__bet //= 2

    def __get_draw(self) -> bool:
        return self.__user_hand.get_summary() == self.__bot.hand.get_summary()

    def __get_user_ace_win(self) -> bool:
        return self.__user_hand.two_ace()

    def __get_bot_ace_win(self) -> bool:
        return self.__bot.hand.two_ace()

    def __get_user_win(self) -> bool:
        return self.__user_hand.get_summary() > self.__bot.hand.get_summary()

    def __get_user_lose(self) -> bool:
        return self.__user_hand.get_summary() > 21

    def __get_bot_lose(self) -> bool:
        return self.__bot.hand.get_summary() > 21

    def __get_user_21(self) -> bool:
        return self.__user_hand.get_summary() == 21

    def __get_bot_21(self) -> bool:
        return self.__bot.hand.get_summary() == 21

    @property
    def cards(self) -> Cards:
        return self.__cards

    @property
    def user_hand(self) -> Hand:
        return self.__user_hand

    @property
    def user_id(self) -> [str, int]:
        return self.__user_id

    @property
    def bot(self) -> BotBlackjack:
        return self.__bot

    @property
    def bet(self) -> int:
        return self.__bet

    @property
    def message_for_user(self):
        return self.__message_for_user

    @property
    def message_for_bot(self):
        return self.__message_for_bot

    @bet.setter
    def bet(self, new_bet) -> None:
        if new_bet <= MIN_BET:
            self.__bet = MIN_BET
        else:
            self.__bet = new_bet

    @message_for_bot.setter
    def message_for_bot(self, msg_4_bot: types.Message) -> None:
        self.__message_for_bot = msg_4_bot

    @message_for_user.setter
    def message_for_user(self, msg_4_user: types.Message) -> None:
        self.__message_for_user = msg_4_user
