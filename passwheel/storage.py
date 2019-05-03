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

    def decrypt_wheel(self):
        if len(self.wheel) == 0:
            return {}
        plaintext = decrypt(self.get_pass(), self.wheel)
        return json.loads(plaintext.decode('utf8'))

    def encrypt_wheel(self, data):
        plaintext = json.dumps(data).encode('utf8')
        ciphertext = encrypt(self.get_pass(), plaintext)
        with open(self.path, 'wb') as f:
            f.write(ciphertext)

    def add_login(self, service, username, password):
        data = self.decrypt_wheel()
        data[service] = data.get(service) or {}
        data[service][username] = password
        self.encrypt_wheel(data)

    def get_login(self, service):
        data = self.decrypt_wheel()
        logins = data.get(service) or {}
        for key, val in logins.items():
            print('username: {key}\npassword: {val}'.format(key=key, val=val))
