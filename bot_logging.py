from sqlite3 import connect


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
        text = '\"' + text + '\"'
        self.__cur.execute(
            '''insert into log(log_date, log_data) values (current_timestamp, ''' + text + ''')'''
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
            '''insert into users(user_id, user_last_name, user_name, user_username) values 
            (''' + str(user_id) + ', ' + user_lastname + ', ' + user_name + ', ' + user_username + ''')'''
        )
        self.__db.commit()

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
        # db: LogDB = LogDB()
        result = None
        out_str: str
        try:
            out_str = 'Calling ' + str(func.__name__) + ' with arguments ' + str(args) + str(kwargs)
            # db.input_log_value(out_str)
            print(out_str)
            result = func(*args, **kwargs)
        except Exception as e:
            # db.input_log_value(str(e))
            print(e)
            return result
        finally:
            out_str = 'Stopping ' + str(func.__name__)
            # db.input_log_value(out_str)
            print(out_str)
            out_str = 'Result: ' + str(result)
            # db.input_log_value(out_str)
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
            # db: LogDB = LogDB()
            result = None
            out_str: str
            try:
                out_str = 'Calling coroutine ' + str(func.__name__) + ' with arguments ' + str(args) + str(kwargs)
                # db.input_log_value(out_str)
                print(out_str)
                result = await func(*args, **kwargs)
            except Exception as e:
                # db.input_log_value(str(e))
                print(e)
                return result
            finally:
                out_str = 'Stopping coroutine ' + str(func.__name__)
                # db.input_log_value(out_str)
                print(out_str)
                out_str = 'Result: ' + str(result)
                # db.input_log_value(out_str)
                print(out_str)
                return result
        return _wrapped
    return _wrapper
