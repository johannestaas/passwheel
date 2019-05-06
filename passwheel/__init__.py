'''
passwheel

A password and secret personal storage tool.
'''

__title__ = 'passwheel'
__version__ = '0.1.0'
__all__ = ('Wheel',)
__author__ = 'Johan Nestaas <johannestaas@gmail.com>'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2019 Johan Nestaas'

from .wheel import Wheel
from .passgen import gen_password
from .clipboard import copy
from .util import info, warning


def main():
    import argparse
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest='cmd')

    p = subs.add_parser('add', help='add a login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', help='login')
    p.add_argument(
        '--custom', '-c', action='store_true',
        help='input custom password',
    )
    p.add_argument(
        '--words', '-w', type=int, default=2,
        help='number of words in generated password',
    )
    p.add_argument(
        '--digits', '-d', type=int, default=3,
        help='number of digits in generated password',
    )
    p.add_argument(
        '--symbol', '-s', action='store_true',
        help='append a random symbol to the password',
    )

    p = subs.add_parser('rm', help='remove a service or login')
    p.add_argument('service', help='service/website')
    p.add_argument('username', nargs='?', default=None, help='login')

    p = subs.add_parser('get', help='fetch creds for service/website')
    p.add_argument('service', help='service/website')

    p = subs.add_parser('dump', help='dump all decrypted credentials')
    p.add_argument(
        '--no-passwords', '-n', action='store_true',
        help='dont print passwords',
    )
    args = parser.parse_args()

    wheel = Wheel()
    if args.cmd == 'dump':
        pw = wheel.get_pass(prompt='unlock: ')
        data = wheel.decrypt_wheel(pw)
        if not data:
            warning('no passwords stored.')
        else:
            for service, logins in data.items():
                print(service)
                for user, pw in logins.items():
                    if args.no_passwords:
                        print('  {}'.format(user))
                    else:
                        print('  {}: {}'.format(user, pw))
    elif args.cmd == 'add':
        if args.custom:
            add_pw = wheel.get_pass(prompt='new password: ', verify=True)
        else:
            add_pw, entropy = gen_password(
                num_words=args.words,
                num_digits=args.digits,
                add_symbol=args.symbol,
            )
            info('generated password with {} bits of entropy'.format(
                int(entropy),
            ))
            if copy(add_pw):
                info('password copied to clipboard')
        wheel.add_login(args.service, args.username, add_pw)
    elif args.cmd == 'rm':
        wheel.rm_login(args.service, args.username)
    elif args.cmd == 'get':
        logins = wheel.get_login(args.service)
        if not logins:
            warning('service {!r} not found'.format(args.service))
        else:
            for key, val in logins:
                print('{}|{}'.format(key, val))
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
