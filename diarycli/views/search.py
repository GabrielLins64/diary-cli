import os
import curses
from diarycli.view import View
from diarycli.views.navigate import Navigate
from diarycli.views.cryptography import Cryptography, CryptographyMode
from diarycli.configs import load_configs
from enum import Enum


class OptionType(Enum):
    ENC_FILE = 0
    DEC_FILE = 1
    OTHER = 2

class Search(View):
    """Search view

    Allow user to find directories and files that are tracked
    by the application.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Buscar'

        self.navigate_view = Navigate()
        self.navigate_view.parent = self
        self.cryptography_view = Cryptography()
        self.cryptography_view.parent = self

        self.path = False
        self.editor = False
        self.searching = False
        self.search_string = ''
        self.leave = False

        self.options = []
        self.options_length = len(self.options)
        self.selected_option = 0
        self.viewport_position = 0
        self.screen_adjustment = 3

    def adjust_viewport(self, interface):
        height = interface.stdscr.getmaxyx()[0]

        if self.selected_option < self.viewport_position:
            self.viewport_position = self.selected_option
        elif self.selected_option >= self.viewport_position + height - self.screen_adjustment:
            self.viewport_position = self.selected_option - height + self.screen_adjustment + 1

        if self.viewport_position < 0:
            self.viewport_position = 0
        elif self.viewport_position > self.options_length - height + self.screen_adjustment:
            self.viewport_position = max(0, self.options_length - height + self.screen_adjustment)

        interface.stdscr.clear()

    def search_files(self, search_string):
        self.options = []
        
        if not self.path or not self.editor:
            configs = load_configs()
            self.path = os.path.expanduser(configs['storage'])
            self.editor = os.path.expanduser(configs['editor'])

        for root, dirs, files in os.walk(self.path):
            for name in dirs:
                if search_string.lower() in name.lower():
                    self.options.append(os.path.join(root, name + '/'))
            for name in files:
                if search_string.lower() in name.lower():
                    self.options.append(os.path.join(root, name))

        self.options.append('Voltar')
        self.options_length = len(self.options)

    def cryptography(self, interface, mode: CryptographyMode):
        self.cryptography_view.update_mode(mode)
        self.cryptography_view.set_path(self.options[self.selected_option])

        interface.stdscr.clear()
        interface.current_view = self.cryptography_view

    def check_selected_option_type(self):
        if (self.selected_option == self.options_length - 1):
            self.selected_option_type = OptionType.OTHER
        elif (self.options[self.selected_option].endswith('.enc')):
            self.selected_option_type = OptionType.ENC_FILE
        elif (self.options[self.selected_option].endswith('/')):
            self.selected_option_type = OptionType.OTHER
        else:
            self.selected_option_type = OptionType.DEC_FILE

    def return_to_search_view(self, interface):
        self.searching = False
        self.search_string = ''
        self.options = []
        self.options_length = 0
        self.selected_option = 0
        self.viewport_position = 0

        interface.stdscr.clear()
        interface.stdscr.refresh()

    def go_back(self, interface):
        self.return_to_search_view(interface)
        interface.go_back()

    def choose_option(self, interface):
        if self.selected_option in range(len(self.options)):
            if self.selected_option == self.options_length - 1:
                self.return_to_search_view(interface)
            else:
                selected_path = self.options[self.selected_option]
                if os.path.isdir(selected_path):
                    self.navigate_view.update_path(selected_path)
                    interface.stdscr.clear()
                    interface.current_view = self.navigate_view
                else:
                    self.navigate_view.editor = self.editor
                    self.navigate_view.open_file(selected_path, interface)

    def render(self, interface):
        if (self.searching):
            interface.stdscr.addstr(0, 1, f'{self.name}: {self.search_string}')
            interface.stdscr.addstr(1, 1, 'Pressione (Q) para voltar à busca')

            self.check_selected_option_type()
            if (self.selected_option_type == OptionType.DEC_FILE or self.selected_option_type == OptionType.ENC_FILE):
                interface.stdscr.addstr(2, 1, f'C - Criptografar. | X - Descriptografar')
                self.screen_adjustment = 4
            else: 
                self.screen_adjustment = 3

            height, width = interface.stdscr.getmaxyx()
            visible_options = self.options[self.viewport_position:self.viewport_position + height - self.screen_adjustment]

            for i, option in enumerate(visible_options):
                option_index = self.viewport_position + i + 1

                if i == self.selected_option - self.viewport_position:
                    interface.stdscr.addstr(i + self.screen_adjustment, 1, f"> {option_index}. {option}")
                else:
                    interface.stdscr.addstr(i + self.screen_adjustment, 1, f"  {option_index}. {option}")

        else:
            curses.echo()

            interface.stdscr.addstr(0, 1, self.name)
            interface.stdscr.addstr(1, 1, 'Deixe o campo "busca" em branco para voltar ao menu.')
            interface.stdscr.addstr(3, 1, 'Busca: ')
            interface.stdscr.move(3, 9)

            new_value = interface.stdscr.getstr().decode('utf-8')

            if (new_value != ''):
                curses.noecho()
                self.enter_search_mode = True
                self.search_string = new_value
                self.search_files(new_value)
            else:
                self.leave = True

    def handle_events(self, interface):
        if (self.leave):
            self.leave = False
            curses.noecho()
            interface.stdscr.clear()
            interface.stdscr.refresh()
            interface.go_back()

        elif self.enter_search_mode:
            self.enter_search_mode = False
            self.searching = True
            interface.stdscr.clear()
            interface.stdscr.refresh()

        elif self.searching:
            key = interface.stdscr.getch()

            if key == ord('q') and self.searching:
                self.return_to_search_view(interface)

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
