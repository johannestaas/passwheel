'''
passwheel

A password and secret personal storage tool.
'''

__title__ = 'passwheel'
__version__ = '0.0.1'
__all__ = ('Wheel',)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'

from .storage import Wheel


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    p = subs.add_parser('dump', help='dump all contents')
    p = subs.add_parser('add', help='add a login')
    p.add_argument('service')
    p.add_argument('username')
    # get password manually
    p = subs.add_parser('rm')
    p.add_argument('service')
    p.add_argument('username')
    p = subs.add_parser('get')
    p.add_argument('service')
    args = parser.parse_args()

    wheel = Wheel()
    if args.cmd == 'dump':
        pw = wheel.get_pass()
        data = wheel.decrypt_wheel(pw)
        for service, logins in data.items():
            print(service)
            for user, pw in logins.items():
                print('  {}: {}'.format(user, pw))
    elif args.cmd == 'add':
        add_pw = wheel.get_pass()
        wheel.add_login(args.service, args.username, add_pw)
    elif args.cmd == 'rm':
        wheel.rm_login(args.service, args.username)
    elif args.cmd == 'get':
        logins = wheel.get_login(args.service)
        for key, val in logins:
            print('username: {key}\npassword: {val}'.format(key=key, val=val))
    else:
        parser.print_usage()

if __name__ == '__main__':
    main()
