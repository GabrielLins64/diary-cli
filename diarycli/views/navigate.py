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
        self.children = []
        self.page = 0

        self.options = [child.name for child in self.children]
        self.options.append("Voltar")
        self.options_length = len(self.options)
        self.selected_option = 0

    def load_data(self, interface):
        with open(CONFIGS_PATH) as f:
            configs = json.load(f)

        if not os.path.exists(configs['storage']):
            interface.stdscr.addstr(4, 1, f"O diretório de armazenamento configurado não foi encontrado.")
            return

    def choose_option(self, interface):
        if (self.selected_option == self.options_length - 1):
            interface.go_back()

    def render(self, interface):
        interface.stdscr.addstr(0, 1, self.name)
        self.load_data(interface)

        for i in range(self.options_length):
            if i == self.selected_option:
                interface.stdscr.addstr(i+2, 1, f"> {i+1}. {self.options[i]}")
            else:
                interface.stdscr.addstr(i+2, 1, f"  {i+1}. {self.options[i]}")

    def handle_events(self, interface):
        key = interface.stdscr.getch()

        if key == curses.KEY_UP:
            self.selected_option = (self.selected_option - 1) % self.options_length

        elif key == curses.KEY_DOWN:
            self.selected_option = (self.selected_option + 1) % self.options_length

        elif key == ord('\n'):
            self.choose_option(interface)

        elif 48 <= key <= 57:
            if int(chr(key)) in range(1, self.options_length + 1):
                self.selected_option = int(chr(key)) - 1
                self.choose_option(interface)
