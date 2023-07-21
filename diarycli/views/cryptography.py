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
        self.configs = None

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
        self.configs = configs.load_configs()
        showPasswd = self.configs.get('showPassword')

        interface.stdscr.addstr(0, 1, f"{self.mode_name}: \"{self.path}\"")
        interface.stdscr.addstr(1, 1, "Insira abaixo suas senhas separadas por espaços.")
        interface.stdscr.addstr(2, 1, "Ou deixe em branco para cancelar.")

        interface.stdscr.addstr(4, 1, "Senhas: ")
        interface.stdscr.refresh()

        curses.curs_set(1)

        passwords = ""
        y, x = 4, 9

        while True:
            char = interface.stdscr.getch()

            if char == ord('\n'):
                break
            elif char == curses.KEY_BACKSPACE or char == 127:
                if passwords:
                    passwords = passwords[:-1]
                    interface.stdscr.addch(y, x + len(passwords), ' ')
                    interface.stdscr.move(y, x + len(passwords))
            elif char == ord(' '):
                passwords += chr(char)
                interface.stdscr.addch(y, x + len(passwords) - 1, ' ')
            else:
                passwords += chr(char)
                interface.stdscr.addch(y, x + len(passwords) - 1, chr(char) if showPasswd else '*')

            interface.stdscr.refresh()

        curses.curs_set(0)
        interface.stdscr.clear()

        if passwords:
            if self.mode == CryptographyMode.ENCRYPT:
                self.encrypt(passwords)
            else:
                self.decrypt(passwords)

        self.leave = True

    def handle_events(self, interface):
        if (self.leave):
            self.leave = False
            curses.noecho()
            interface.stdscr.clear()
            interface.stdscr.refresh()
            interface.go_back()
