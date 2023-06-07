import os
import json
from diarycli.view import View
import curses


CONFIGS_PATH = "configs.json"


class Navigate(View):
    """Navigation view

    Allow user to navigate between directories and files
    tracked by the application.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Navegar'

        self.initial_path = False
        self.current_path = False
        self.directories = []
        self.files = []

        self.options = []
        self.options_length = len(self.options)
        self.selected_option = 0
        self.viewport_position = 0

    def adjust_viewport(self, interface):
        height = interface.stdscr.getmaxyx()[0]
        if self.selected_option < self.viewport_position:
            self.viewport_position = self.selected_option
        elif self.selected_option >= self.viewport_position + height - 4:
            self.viewport_position = self.selected_option - height + 5

        if self.viewport_position < 0:
            self.viewport_position = 0
        elif self.viewport_position > self.options_length - height + 4:
            self.viewport_position = max(0, self.options_length - height + 4)

    def load_path(self, interface):
        if not self.initial_path:
            with open(CONFIGS_PATH) as f:
                configs = json.load(f)
                self.initial_path = configs['storage']
                self.current_path = configs['storage']

        if os.path.exists(self.current_path):
            self.scan_directory(interface)
        else:
            interface.stdscr.addstr(4, 1, f"O diretório {self.current_path} está inacessível ou não existe.")

    def scan_directory(self, interface):
        self.options = []

        for entry in os.scandir(self.current_path):
            if entry.is_dir():
                self.options.append(entry.name + '/')
            else:
                self.options.append(entry.name)

        self.options.append('Voltar')
        self.options_length = len(self.options)

        self.adjust_viewport(interface)
        interface.stdscr.clear()

    def previous_directory(self):
        self.current_path = self.current_path[:self.current_path.rstrip('/').rindex('/') + 1]

    def go_back(self, interface):
        interface.stdscr.clear()

        if (self.current_path == self.initial_path):
            interface.go_back()
        else:
            self.previous_directory()

    def open_file(self, path):
        pass

    def choose_option(self, interface):
        if (self.selected_option in range(len(self.options))):
            if self.selected_option == self.options_length - 1:
                self.selected_option = 0
                self.viewport_position = 0
                self.go_back(interface)
            else:
                option = self.options[self.selected_option]

                if (option.endswith('/')):
                    self.selected_option = 0
                    self.viewport_position = 0
                    self.current_path += option
                else:
                    self.open_file(self.current_path + option)

    def render(self, interface):
        self.load_path(interface)

        interface.stdscr.addstr(0, 1, self.name)
        interface.stdscr.addstr(1, 1, f'Diretório atual: "{self.current_path}"')
        interface.stdscr.addstr(2, 1, 'Pressione (Q) para sair da navegação.')

        height, width = interface.stdscr.getmaxyx()
        visible_options = self.options[self.viewport_position:self.viewport_position+height-4]

        for i, option in enumerate(visible_options):
            option_index = self.viewport_position + i + 1

            if i == self.selected_option - self.viewport_position:
                interface.stdscr.addstr(i+4, 1, f"> {option_index}. {option}")
            else:
                interface.stdscr.addstr(i+4, 1, f"  {option_index}. {option}")

        interface.stdscr.refresh()

    def handle_events(self, interface):
        key = interface.stdscr.getch()

        if key == ord('q') or not self.options:
            self.current_path = self.initial_path
            interface.stdscr.clear()
            interface.go_back()

        elif key == curses.KEY_UP:
            self.selected_option = (self.selected_option - 1) % self.options_length
            self.adjust_viewport(interface)

        elif key == curses.KEY_DOWN:
            self.selected_option = (self.selected_option + 1) % self.options_length
            self.adjust_viewport(interface)

        elif key == ord('\n'):
            self.choose_option(interface)

        elif 48 <= key <= 57:
            if int(chr(key)) in range(1, self.options_length + 1):
                self.selected_option = int(chr(key)) - 1
                self.choose_option(interface)
