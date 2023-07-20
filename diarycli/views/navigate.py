import subprocess
import os
from diarycli.view import View
from diarycli.views.create import Create, CreateMode
from diarycli.views.cryptography import Cryptography, CryptographyMode
import curses
from diarycli.configs import load_configs
from enum import Enum


class OptionType(Enum):
    ENC_FILE = 0
    DEC_FILE = 1
    OTHER = 2

class Navigate(View):
    """Navigation view

    Allow user to navigate between directories and files
    tracked by the application.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Navegar'

        self.create_view = Create()
        self.create_view.parent = self
        self.cryptography_view = Cryptography()
        self.cryptography_view.parent = self

        self.initial_path = False
        self.current_path = False
        self.editor = False
        self.directories = []
        self.files = []

        self.options = []
        self.options_length = len(self.options)
        self.selected_option = 0
        self.viewport_position = 0
        self.selected_option_type = OptionType.OTHER

    def initialize_configs(self, interface):
        configs = load_configs()
        self.initial_path = os.path.expanduser(configs['storage'])
        self.editor = configs['editor']

        if not os.path.exists(self.initial_path):
            interface.stdscr.addstr(5, 1, f"O diretório base {self.initial_path} está inacessível ou não existe.")
            self.initial_path = False

    def reset_configs(self):
        self.initial_path = False
        self.current_path = False
        self.options = []

    def scan_directory(self):
        self.options = []

        for entry in os.scandir(self.current_path):
            if entry.is_dir():
                self.options.append(entry.name + '/')
            else:
                self.options.append(entry.name)

        self.options.append('Voltar')
        self.options_length = len(self.options)

    def update_path(self, new_path: str):
        self.selected_option = 0
        self.viewport_position = 0
        self.current_path = new_path
        self.scan_directory()

    def previous_directory(self):
        self.current_path = self.current_path[:self.current_path.rstrip('/').rindex('/') + 1]
        self.scan_directory()

    def go_back(self, interface):
        interface.stdscr.clear()

        if (self.current_path == self.initial_path):
            self.reset_configs()
            interface.go_back()
        else:
            self.previous_directory()

    def open_file(self, path, interface):
        try:
            if not self.editor:
                raise FileNotFoundError

            curses.endwin()
            subprocess.run([self.editor, path])
            curses.doupdate()
        except FileNotFoundError:
            interface.stdscr.clear()
            interface.stdscr.addstr(1, 1, f'Erro: o editor "{self.editor}" não está disponível.')
            interface.stdscr.getch()

    def create_directory(self, interface):
        self.create_view.update_mode(CreateMode.DIRECTORY)
        self.create_view.set_path(self.current_path)

        self.scan_directory()
        interface.stdscr.clear()
        interface.current_view = self.create_view

    def create_file(self, interface):
        self.create_view.update_mode(CreateMode.FILE)
        self.create_view.set_path(self.current_path)

        interface.stdscr.clear()
        interface.current_view = self.create_view

    def cryptography(self, interface, mode: CryptographyMode):
        self.cryptography_view.update_mode(mode)
        self.cryptography_view.set_path(f"{self.current_path}{self.options[self.selected_option]}")

        interface.stdscr.clear()
        interface.current_view = self.cryptography_view

    def choose_option(self, interface):
        if (self.selected_option in range(len(self.options))):
            if self.selected_option == self.options_length - 1:
                self.selected_option = 0
                self.viewport_position = 0
                self.go_back(interface)
            else:
                option = self.options[self.selected_option]

                if (option.endswith('/')):
                    new_path = self.current_path + option
                    self.update_path(new_path)
                    interface.stdscr.clear()
                else:
                    self.open_file(self.current_path + option, interface)

    def adjust_viewport(self, interface):
        height = interface.stdscr.getmaxyx()[0]

        if self.selected_option < self.viewport_position:
            self.viewport_position = self.selected_option
        elif self.selected_option >= self.viewport_position + height - 5:
            self.viewport_position = self.selected_option - height + 6

        if self.viewport_position < 0:
            self.viewport_position = 0
        elif self.viewport_position > self.options_length - height + 5:
            self.viewport_position = max(0, self.options_length - height + 5)

        interface.stdscr.clear()

    def check_selected_option_type(self):
        if (not self.options_length):
            return

        if (self.selected_option == self.options_length - 1):
            self.selected_option_type = OptionType.OTHER
        elif (self.options[self.selected_option].endswith('.enc')):
            self.selected_option_type = OptionType.ENC_FILE
        elif (self.options[self.selected_option].endswith('/')):
            self.selected_option_type = OptionType.OTHER
        else:
            self.selected_option_type = OptionType.DEC_FILE

    def render(self, interface):
        if not self.initial_path:
            self.initialize_configs(interface)

        if self.initial_path:
            if not self.current_path:
                self.update_path(self.initial_path)

        self.check_selected_option_type()
        interface.stdscr.addstr(0, 1, f'{self.name}')
        interface.stdscr.addstr(1, 1, 'Q - Sair.')
        interface.stdscr.addstr(2, 1, 'D - Criar um diretório   | F - Criar um arquivo.')

        if (self.selected_option_type == OptionType.DEC_FILE or self.selected_option_type == OptionType.ENC_FILE):
            interface.stdscr.addstr(3, 1, f'C - Criptografar.        | X - Descriptografar')

        if self.initial_path:
            interface.stdscr.addstr(0, 9, f': {self.current_path}')

            height, width = interface.stdscr.getmaxyx()
            visible_options = self.options[self.viewport_position:self.viewport_position+height-5]

            for i, option in enumerate(visible_options):
                option_index = self.viewport_position + i + 1

                if i == self.selected_option - self.viewport_position:
                    interface.stdscr.addstr(i+5, 1, f"> {option_index}. {option}")
                else:
                    interface.stdscr.addstr(i+5, 1, f"  {option_index}. {option}")

    def handle_events(self, interface):
        key = interface.stdscr.getch()

        if key == ord('q') or not self.options:
            self.reset_configs()
            interface.stdscr.clear()
            interface.go_back()

        elif key == ord('d'):
            self.create_directory(interface)

        elif key == ord('f'):
            self.create_file(interface)

        elif key == curses.KEY_UP:
            self.selected_option = (self.selected_option - 1) % self.options_length
            self.adjust_viewport(interface)

        elif key == curses.KEY_DOWN:
            self.selected_option = (self.selected_option + 1) % self.options_length
            self.adjust_viewport(interface)

        elif key == ord('c'):
            self.cryptography(interface, CryptographyMode.ENCRYPT)

        elif key == ord('x'):
            self.cryptography(interface, CryptographyMode.DECRYPT)

        elif key == ord('\n'):
            self.choose_option(interface)

        elif 48 <= key <= 57:
            if int(chr(key)) in range(1, self.options_length + 1):
                self.selected_option = int(chr(key)) - 1
                self.choose_option(interface)
