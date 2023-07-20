from diarycli.view import View
import curses
from diarycli import configs, cryptography
from enum import Enum
import os


class CryptographyMode(Enum):
    ENCRYPT = 1
    DECRYPT = 2


class Cryptography(View):
    """Create view

    Let user to create a file or a directory.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Criar'
        self.mode = CryptographyMode.ENCRYPT
        self.mode_name = 'diretório'
        self.path = False
        self.leave = False
        self.salt = ''

    def load_salt(self):
        cfg = configs.load_configs()
        if os.path.exists(cfg.get('saltLocation')):
            with open(cfg.get('saltLocation')) as f:
                self.salt = f.read()

    def update_mode(self, new_mode: CryptographyMode):
        self.mode = new_mode
        self.mode_name = 'Criptografar' if new_mode == CryptographyMode.ENCRYPT else 'Decriptografar'

    def set_path(self, path: str):
        self.path = path

    def encrypt(self, password: str):
        if not self.path:
            return

        cryptography.encrypt(self.path, password, self.salt)

    def decrypt(self, password: str):
        if not self.path:
            return

        cryptography.decrypt(self.path, password, self.salt)

    def render(self, interface):
        curses.echo()

        interface.stdscr.addstr(0, 1, f"{self.mode_name}: \"{self.path}\"")
        interface.stdscr.addstr(1, 1, f"Insira abaixo suas senhas separadas por espaços.")
        interface.stdscr.addstr(2, 1, f"Ou deixe em branco para cancelar.")

        interface.stdscr.addstr(4, 1, f"Senhas: ")
        interface.stdscr.move(4, 9)

        new_value = interface.stdscr.getstr().decode('utf-8')
        interface.stdscr.clear()
        
        if new_value != '':
            if self.mode == CryptographyMode.ENCRYPT:
                self.encrypt(new_value)
            else:
                self.decrypt(new_value)

        self.leave = True

    def handle_events(self, interface):
        if (self.leave):
            self.leave = False
            curses.noecho()
            interface.stdscr.clear()
            interface.stdscr.refresh()
            self.parent.scan_directory()
            interface.go_back()
