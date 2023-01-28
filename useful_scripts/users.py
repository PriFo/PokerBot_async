
def main():
    with open(
        'ids.txt',
        'r',
        encoding='utf-8'
    ) as f:
        users = ''
        while True:
            user = f.readline()
            if user == '':
                break
            if users != '':
                users += ',\n'
            user = '(' + user.replace(' |', ',').replace('\n', '') + ')'
            users += user
        print(users)


if __name__ == '__main__':
    main()
