import os
import sys
import json
from getpass import getpass

from fuzzywuzzy.fuzz import ratio
from nacl.exceptions import CryptoError

from .util import error
from .crypto import encrypt, decrypt

# Should match at least this much ratio with fuzzy string matching.
RATIO = 85
DEFAULT_LOCKED = os.path.expanduser('~/.passwheel')
DEFAULT_UNLOCKED = os.path.expanduser('~/.passwheel.json')


class Wheel:
    def __init__(self):
        self.wheel = None
        self.load_or_create_wheel()

    @property
    def path(self):
        """
        If in the future, we support a different path.
        """
        return DEFAULT_LOCKED

    def load_or_create_wheel(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                self.wheel = f.read()
        else:
            self.wheel = self.create_wheel()

    def create_wheel(self):
        print(
            '{} doesnt exist, initializing.\n'
            'Please create master password.'.format(self.path)
        )
        pw = self.get_pass(prompt='master password: ', verify=True)
        self.wheel = self.encrypt_wheel({}, pw)

    def get_unlock_pw(self):
        return self.get_pass(prompt='unlock: ')

    def get_pass(self, prompt=None, verify=False):
        if not prompt:
            prompt = 'password: '
        while True:
            pw = getpass(prompt).encode('utf8')
            if not verify:
                return pw
            pw2 = getpass('verify {}'.format(prompt)).encode('utf8')
            if pw == pw2:
                return pw
            print('password mismatch')

    def decrypt_wheel(self, pw=None):
        if pw is None:
            if os.path.isfile(DEFAULT_UNLOCKED):
                with open(DEFAULT_UNLOCKED) as f:
                    return json.load(f)
            else:
                error('password is None but no unlocked wheel exists')
                sys.exit(1)
        try:
            plaintext = decrypt(pw, self.wheel)
        except CryptoError:
            error('unlock failed!')
            sys.exit(1)
        return json.loads(plaintext.decode('utf8'))

    def encrypt_wheel(self, data, pw):
        plaintext = json.dumps(data).encode('utf8')
        ciphertext = encrypt(pw, plaintext)
        with open(self.path, 'wb') as f:
            f.write(ciphertext)
        return ciphertext

    def add_login(self, service, username, password):
        pw = self.get_unlock_pw()
        data = self.decrypt_wheel(pw=pw)
        data[service] = data.get(service) or {}
        if isinstance(password, bytes):
            password = password.decode('utf8')
        data[service][username] = password
        self.wheel = self.encrypt_wheel(data, pw)

    def change_password(self):
        pw = self.get_unlock_pw()
        data = self.decrypt_wheel(pw=pw)
        new_pw = self.get_pass(prompt='new master password: ', verify=True)
        self.wheel = self.encrypt_wheel(data, new_pw)

    def get_login(self, service):
        if os.path.isfile(DEFAULT_UNLOCKED):
            data = self.decrypt_wheel()
            return data.get(service) or {}
        pw = self.get_unlock_pw()
        data = self.decrypt_wheel(pw=pw)
        return data.get(service) or {}

    def find_login(self, query):
        pw = None
        if not os.path.isfile(DEFAULT_UNLOCKED):
            pw = self.get_unlock_pw()
        data = self.decrypt_wheel(pw=pw)
        ratios = sorted(
            (
                (ratio(query, key), key)
                for key in data
            ),
            reverse=True,
        )
        threshold = min(RATIO, ratios[0][0])
        top = [
            key
            for r, key in ratios
            if r >= threshold
        ]
        return [
            (key, data[key])
            for key in top
        ]

    def rm_login(self, service, login):
        pw = self.get_unlock_pw()
        data = self.decrypt_wheel(pw=pw)
        if login is None:
            del data[service]
        else:
            del data[service][login]
            if not data[service]:
                del data[service]
        self.wheel = self.encrypt_wheel(data, pw)

    def unlock_wheel(self, pw):
        try:
            plaintext = decrypt(pw, self.wheel)
        except CryptoError:
            error('unlock failed!')
            sys.exit(1)
        os.umask(0o177)
        with open(DEFAULT_UNLOCKED, 'wb') as f:
            f.write(plaintext)
        return DEFAULT_UNLOCKED

    def lock_wheel(self):
        if os.path.isfile(DEFAULT_UNLOCKED):
            os.remove(DEFAULT_UNLOCKED)
