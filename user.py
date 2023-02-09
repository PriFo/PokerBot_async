from bot_logging import LogDB


class Profile(object):

    def __init__(self, user_id: [str, int]):
        self.__wins_poker = None
        self.__wins_blackjack = None
        self.__count_poker = None
        self.__count_blackjack = None
        self.__level = None
        self.__exp = None
        self.__money = None
        self.__user_id = None
        profile = LogDB().get_profile_value(user_id)
        if profile:
            self.__read_profile(profile)
        else:
            self.__create_new_profile(user_id)

    def __hash__(self):
        return hash((
            self.__user_id,
            self.__exp,
            self.__level,
            self.__money,
            self.__count_poker,
            self.__count_blackjack,
            self.__wins_blackjack,
            self.__wins_poker
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

    def __read_profile(self, profile_info: dict):
        self.__user_id = profile_info.get('id')
        self.__money = profile_info.get('money')
        self.__level = profile_info.get('level')
        self.__exp = profile_info.get('exp')
        self.__count_blackjack = profile_info.get('count_blackjack')
        self.__count_poker = profile_info.get('count_poker')
        self.__wins_blackjack = profile_info.get('wins_blackjack')
        self.__wins_poker = profile_info.get('wins_poker')

    def __create_new_profile(self, user_id: [str, int]):
        LogDB().input_profile_value(user_id=user_id)
        self.__read_profile(LogDB().get_profile_value(user_id=user_id))
