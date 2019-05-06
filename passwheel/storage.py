import os
import json
from getpass import getpass
from subprocess import check_output

from .crypto import encrypt, decrypt


class Wheel:
    def __init__(self):
        self.wheel = None
        self.load_or_create_wheel()

    @property
    def path(self):
        return os.path.expanduser('~/.passwheel')

    def load_or_create_wheel(self):
        if os.path.exists(self.path):
            with open(self.path, 'rb') as f:
                self.wheel = f.read()
        else:
            with open(self.path, 'wb') as f:
                f.write(b'')
            self.wheel = b''

    def get_pass(self):
        return getpass().encode('utf8')

    def random_password(self):
        return check_output(['passgen', '-w', '2']).strip()

    def decrypt_wheel(self, pw):
        if len(self.wheel) == 0:
            return {}
        plaintext = decrypt(pw, self.wheel)
        return json.loads(plaintext.decode('utf8'))

    def encrypt_wheel(self, data, pw):
        plaintext = json.dumps(data).encode('utf8')
        ciphertext = encrypt(pw, plaintext)
        with open(self.path, 'wb') as f:
            f.write(ciphertext)

    def add_login(self, service, username, password):
        pw = self.get_pass()
        data = self.decrypt_wheel(pw)
        data[service] = data.get(service) or {}
        if isinstance(password, bytes):
            password = password.decode('utf8')
        data[service][username] = password
        self.encrypt_wheel(data, pw)

    def get_login(self, service):
        pw = self.get_pass()
        data = self.decrypt_wheel(pw)
        logins = data.get(service) or {}
        return logins.items()

    def rm_login(self, service, login):
        pw = self.get_pass()
        data = self.decrypt_wheel(pw)
        del data[service][login]
        self.encrypt_wheel(data, pw)
