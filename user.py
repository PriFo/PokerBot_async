from datetime import date, timedelta, datetime

from bot_logging import LogDB


BONUS: int = 1200
LVL_BONUS: int = 2000
EXP_MULTIPLIER: int = 50
BLACKJACK_WIN_EXP_BOOST: int = 5
BLACKJACK_GAME_EXP_BOOST: int = 2
POKER_WIN_EXP_BOOST: int = 10
POKER_GAME_EXP_BOOST: int = 3


class Profile(object):

    def __init__(self, user_id: [str, int]):
        self.__bonus_date: [date, None] = None
        self.__wins_poker: [int, None] = None
        self.__wins_blackjack: [int, None] = None
        self.__count_poker: [int, None] = None
        self.__count_blackjack: [int, None] = None
        self.__level: [int, None] = None
        self.__exp: [int, None] = None
        self.__money: [int, None] = None
        self.__username: [str, None] = None
        self.__user_id: [int, str, None] = None
        profile: [dict, None] = LogDB().get_profile_value(user_id)
        if profile:
            self.__read_profile(profile)
        else:
            self.__create_new_profile(user_id)

    def get_dict(self):
        return {
            'money': self.__money,
            'username': self.__username,
            'user_id': self.__user_id,
            'exp': self.__exp,
            'level': self.__level,
            'bonus_date': self.__bonus_date,
            'wins_poker': self.__wins_poker,
            'count_poker': self.__count_poker,
            'wins_blackjack': self.__wins_blackjack,
            'count_blackjack': self.__count_blackjack
        }

    def __hash__(self):
        return hash((
            self.__user_id,
            self.__exp,
            self.__level,
            self.__money,
            self.__count_poker,
            self.__count_blackjack,
            self.__wins_blackjack,
            self.__wins_poker,
            self.__bonus_date
        ))

    def __str__(self):
        out_str = f'user_id: {self.__user_id}\nexp: {self.__exp}\nlevel: {self.__level}\n' \
                  f'money: {self.__money}\ncount_poker: {self.__count_poker}\n' \
                  f'count_blackjack: {self.__count_blackjack}\nwins_poker: {self.__wins_poker}\n' \
                  f'wins_blackjack: {self.__wins_blackjack}'
        return out_str

    @property
    def user_id(self):
        return self.__user_id

    @property
    def level(self):
        return self.__level

    @property
    def exp(self):
        return self.__exp

    @property
    def money(self):
        return self.__money

    @property
    def count_blackjack(self):
        return self.__count_blackjack

    @property
    def count_poker(self):
        return self.__count_poker

    @property
    def wins_poker(self):
        return self.__wins_poker

    @property
    def wins_blackjack(self):
        return self.__wins_blackjack

    @property
    def bonus_date(self):
        return self.__bonus_date

    @property
    def username(self):
        return self.__username

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    @money.setter
    def money(self, value):
        self.__money = value

    @exp.setter
    def exp(self, value):
        self.__exp = value

    @level.setter
    def level(self, value):
        self.__level = value

    @count_blackjack.setter
    def count_blackjack(self, value):
        self.__count_blackjack = value

    @count_poker.setter
    def count_poker(self, value):
        self.__count_poker = value

    @wins_blackjack.setter
    def wins_blackjack(self, value):
        self.__wins_blackjack = value

    @wins_poker.setter
    def wins_poker(self, value):
        self.__wins_poker = value

    @bonus_date.setter
    def bonus_date(self, value):
        self.__bonus_date = value

    @username.setter
    def username(self, value):
        self.__username = value

    def __read_profile(self, profile_info: dict):
        self.__user_id = profile_info.get('id')
        self.__username = profile_info.get('username')
        self.__money = profile_info.get('money')
        self.__level = profile_info.get('level')
        self.__exp = profile_info.get('exp')
        self.__count_blackjack = profile_info.get('count_blackjack')
        self.__count_poker = profile_info.get('count_poker')
        self.__wins_blackjack = profile_info.get('wins_blackjack')
        self.__wins_poker = profile_info.get('wins_poker')
        self.__bonus_date = datetime.strptime(
            profile_info.get('bonus_date')[:profile_info.get('bonus_date').find('.')], '%Y-%m-%d %H:%M:%S')

    def __create_new_profile(self, user_id: [str, int]):
        LogDB().input_profile_value(user_id=user_id)
        self.__read_profile(LogDB().get_profile_value(user_id=user_id))

    def get_bonus(self) -> bool:
        if (datetime.now() - self.__bonus_date) > timedelta(hours=12):
            self.__money += 12000
            self.__bonus_date = datetime.now()
            return True
        else:
            return False

    def get_exp_for_next_level(self) -> int:
        return self.__level * EXP_MULTIPLIER

    def blackjack_win_exp_add(self):
        self.__exp += BLACKJACK_WIN_EXP_BOOST

    def blackjack_game_exp_add(self):
        self.__exp += BLACKJACK_GAME_EXP_BOOST

    def poker_win_exp_add(self):
        self.__exp += POKER_WIN_EXP_BOOST

    def poker_game_exp_add(self):
        self.__exp += POKER_GAME_EXP_BOOST

    def level_up(self) -> None:
        self.__level += 1
        self.__money += LVL_BONUS
