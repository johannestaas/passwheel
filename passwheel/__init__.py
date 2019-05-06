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
from .passgen import gen_password


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')
    p = subs.add_parser('dump', help='dump all decrypted credentials')
    p.add_argument(
        '--no-passwords', '-n', action='store_true',
        help='dont print passwords',
    )
    p = subs.add_parser('add', help='add a login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', help='login')
    p.add_argument('--gen-password', '-g', action='store_true')
    # get password manually
    p = subs.add_parser('rm', help='remove a service or login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', nargs='?', default=None, help='login')
    p = subs.add_parser('get', help='fetch creds for service/website')
    p.add_argument('service', help='service/website')
    args = parser.parse_args()

    wheel = Wheel()
    if args.cmd == 'dump':
        pw = wheel.get_pass(prompt='unlock: ')
        data = wheel.decrypt_wheel(pw)
        for service, logins in data.items():
            print(service)
            for user, pw in logins.items():
                if args.no_passwords:
                    print('  {}'.format(user))
                else:
                    print('  {}: {}'.format(user, pw))
    elif args.cmd == 'add':
        if args.gen_password:
            add_pw = gen_password(2, 3)
        else:
            add_pw = wheel.get_pass(prompt='new password: ', verify=True)
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
