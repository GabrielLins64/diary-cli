from diarycli.view import View
import curses
from diarycli import configs
from enum import Enum
import os
import re


class CreateMode(Enum):
    DIRECTORY = 1
    FILE = 2


class Create(View):
    """Create view

    Let user to create a file or a directory.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Criar'
        self.mode = CreateMode.DIRECTORY
        self.mode_name = 'diretório'
        self.path = False
        self.leave = False

    def update_mode(self, new_mode: CreateMode):
        self.mode = new_mode
        self.mode_name = 'diretório' if new_mode == CreateMode.DIRECTORY else 'arquivo'

    def validate_name(self, name: str):
        self.path += '' if self.path.endswith('/') else '/'

        invalid_chars = r'[\\/:\*\?"<>\|]'
        if re.search(invalid_chars, name):
            return False

        if os.path.isfile(self.path + name) or os.path.isdir(self.path + name):
            return False

        reserved_words = [
            'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4',
            'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3',
            'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        ]
        if name.upper() in reserved_words:
            return False

        return True

    def set_path(self, path: str):
        self.path = path

    def create(self, name):
        if not self.path:
            return

        self.path += '' if self.path.endswith('/') else '/'

        if (self.mode == CreateMode.DIRECTORY):
            os.mkdir(self.path + name)
        else:
            open(self.path + name, mode='a').close()

    def render(self, interface):
        curses.echo()

        interface.stdscr.addstr(0, 1, f"Criar {self.mode_name}.")
        interface.stdscr.addstr(1, 1, f"Insira abaixo o nome do {self.mode_name} ou deixe vazio para cancelar.")

        interface.stdscr.addstr(3, 1, f"Nome: ")
        interface.stdscr.move(3, 7)

        new_value = interface.stdscr.getstr().decode('utf-8')
        interface.stdscr.clear()

        if (new_value != ''):
            if (not self.validate_name(new_value)):
                interface.stdscr.addstr(5, 1, f"O nome de {self.mode_name} é inválido ou já existe.")
                return
            self.create(new_value)

        self.leave = True

    def handle_events(self, interface):
        if (self.leave):
            self.leave = False
            curses.noecho()
            interface.stdscr.clear()
            interface.stdscr.refresh()
            self.parent.scan_directory()
            interface.go_back()
