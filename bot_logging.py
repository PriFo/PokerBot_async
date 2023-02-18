from sqlite3 import connect
from traceback import format_exc


class LogDB:

    def __init__(self):
        self.__db = connect('log.sqlite')
        self.__cur = self.__db.cursor()

    def input_log_value(self, text: str) -> None:
        """
        Inserting log info into 'log' table
        :param text: Log's text
        :return: None
        """
        text = '\'' + text.replace('\'', '_').replace('\"', '_') + '\''
        self.__cur.execute(
            f'''insert into log(log_date, log_data) values 
                (current_timestamp, {text})'''
        )
        self.__db.commit()

    def input_user_value(
            self,
            user_id: [str, int],
            user_name: str,
            user_lastname: str = None,
            user_username: str = None
    ) -> None:
        """
        Inserting user info into 'users' table
        :param user_id: User's id
        :param user_name: User's name
        :param user_lastname: User's lastname
        :param user_username: User's username
        :return: None
        """
        self.__cur.execute(
            f'''insert into users(user_id, user_last_name, user_name, user_username) values 
            ('{str(user_id)}', '{user_lastname}', '{user_name}', '{user_username}')'''
        )
        self.__db.commit()

    def input_profile_value(self, user_id: [str, int], username: str = None) -> None:
        if username:
            self.__cur.execute(
                f"""insert into profiles(profile_user_id, profile_username) values 
                    ('{str(user_id)}', '{str(username)}')"""
            )
            self.__db.commit()
        else:
            self.__cur.execute(
                f"""insert into profiles(profile_user_id, profile_username) values 
                ('{str(user_id)}', '{str(user_id)}')"""
            )
            self.__db.commit()

    def update_profile_info(self, profile_info: dict):
        print('try to updating\n', profile_info)
        self.__cur.execute(
            f"""update profiles set 
                profile_username='{profile_info.get('username')}',
                profile_money='{str(profile_info.get('money'))}',
                profile_exp='{str(profile_info.get('exp'))}',
                profile_level='{str(profile_info.get('level'))}',
                count_blackjack='{str(profile_info.get('count_blackjack'))}',
                count_poker='{str(profile_info.get('count_poker'))}',
                wins_blackjack='{str(profile_info.get('wins_blackjack'))}',
                wins_poker='{str(profile_info.get('wins_poker'))}',
                bonus_date='{str(profile_info.get('bonus_date'))}'
                where profile_user_id='{str(profile_info.get('user_id'))}'"""
        )
        self.__db.commit()

    def get_user_value(self, user_id: [str, int]) -> [dict, None]:
        """
        Getting user info from DB
        :param user_id
        :return:
        """
        self.__cur.execute(
            f"""select user_last_name,
            user_name,
            user_username
            from users
            where user_id='{str(user_id)}'"""
        )
        result_list: list = self.__cur.fetchall()
        if result_list:
            result: dict = {
                'id': str(user_id),
                'last_name': result_list[0],
                'name': result_list[1],
                'username': result_list[2]
            }
            return result
        else:
            return None

    def get_profile_value(self, user_id: [str, int]) -> [dict, None]:
        self.__cur.execute(
            f"""select profile_money, 
                profile_level, 
                profile_exp, 
                count_blackjack, 
                count_poker, 
                wins_blackjack, 
                wins_poker,
                bonus_date,
                profile_username
                from profiles 
                where profile_user_id='{str(user_id)}'"""
        )
        result_list: list = self.__cur.fetchall()
        if result_list:
            result_list = result_list.pop(0)
            result: dict = {
                'id': str(user_id),
                'money': result_list[0],
                'level': result_list[1],
                'exp': result_list[2],
                'count_blackjack': result_list[3],
                'count_poker': result_list[4],
                'wins_blackjack': result_list[5],
                'wins_poker': result_list[6],
                'bonus_date': result_list[7],
                'username': result_list[8]
            }
            return result
        else:
            return None

    def do_script(self, script: str):
        self.__cur.execute(
            script
        )
        self.__db.commit()

    def get_logs(self) -> list:
        """
        Getting all data from log
        :return: List of logs
        """
        self.__cur.execute(
            """select * from log"""
        )
        result = self.__cur.fetchall()
        return result

    def get_promos(self):
        self.__cur.execute("""select * from promo""")
        result: list = self.__cur.fetchall()
        return result

    def get_ids(self):
        self.__cur.execute("""select user_id from users""")
        result: list = self.__cur.fetchall()
        return result

    def trunc_logs(self):
        """
        Delete all data from logs
        :return: None
        """
        self.__cur.execute(
            """delete from log where log_id"""
        )
        self.__db.commit()

    def __del__(self):
        """
        Closing connection to database
        :return: None
        """
        self.__cur.close()
        self.__db.close()


def print_func(func):
    """
    Decorator of synchronous functions to collect logs
    :param func: Function
    :return: Result of function
    """
    def _wrapper(*args, **kwargs):
        db: LogDB = LogDB()
        result = None
        out_str: str
        try:
            out_str = f'Calling {str(func.__name__)} with arguments {str(args)} {str(kwargs)}'
            db.input_log_value(out_str)
            print(out_str)
            result = func(*args, **kwargs)
        except Exception as e:
            db.input_log_value(str(e))
            print(format_exc(), e)
            return result
        finally:
            out_str = f'Stopping {str(func.__name__)}'
            db.input_log_value(out_str)
            print(out_str)
            out_str = f'Result: {str(result)}'
            db.input_log_value(out_str)
            print(out_str)
            return result

    return _wrapper


def print_async_func():
    """
    Decorator of asynchronous functions to collect logs
    :return: Result of function
    """
    def _wrapper(func):
        async def _wrapped(*args, **kwargs):
            db: LogDB = LogDB()
            result = None
            out_str: str
            try:
                out_str = f'Calling coroutine {str(func.__name__)} with arguments {str(args)} {str(kwargs)}'
                db.input_log_value(out_str)
                print(out_str)
                result = await func(*args, **kwargs)
            except Exception as e:
                db.input_log_value(str(e))
                print(format_exc(), e)
                return result
            finally:
                out_str = f'Stopping coroutine {str(func.__name__)}'
                db.input_log_value(out_str)
                print(out_str)
                out_str = f'Result: {str(result)}'
                db.input_log_value(out_str)
                print(out_str)
                return result
        return _wrapped
    return _wrapper
