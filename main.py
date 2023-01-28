from asyncio import run
from sys import argv

from bot import start_bot
from bot_logging import print_func, print_async_func


@print_func
def get_dict_argv():
    kwargs: dict = {
        'dev': False,
    }
    for i in argv[1:]:
        if i == '-dev':
            kwargs['dev'] = True
    return kwargs


@print_func
def main(*args):
    args = args[0]
    try:
        start_bot()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main(get_dict_argv())
