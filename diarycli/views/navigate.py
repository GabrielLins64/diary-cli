import os
from diarycli.view import View
from diarycli.views.create import Create, CreateMode
import curses
from diarycli.configs import load_configs


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

        self.initial_path = False
        self.current_path = False
        self.directories = []
        self.files = []

        self.options = []
        self.options_length = len(self.options)
        self.selected_option = 0
        self.viewport_position = 0
        self.header = [
            self.name,
            'Pressione (Q) para sair da navegação.',
            'Pressione (D) para criar um diretório no caminho atual.',
            'Pressione (F) para criar um arquivo no caminho atual.',
        ]
        self.header_size = len(self.header) + 1

    def adjust_viewport(self, interface):
        height = interface.stdscr.getmaxyx()[0]
        if self.selected_option < self.viewport_position:
            self.viewport_position = self.selected_option
        elif self.selected_option >= self.viewport_position + height - self.header_size:
            self.viewport_position = self.selected_option - height + self.header_size + 1

        if self.viewport_position < 0:
            self.viewport_position = 0
        elif self.viewport_position > self.options_length - height + self.header_size:
            self.viewport_position = max(0, self.options_length - height + self.header_size)

    def load_path(self, interface):
        if not self.initial_path:
            configs = load_configs()
            self.initial_path = os.path.expanduser(configs['storage'])
            self.current_path = os.path.expanduser(configs['storage'])

        if os.path.exists(self.current_path):
            self.scan_directory(interface)
        else:
            interface.stdscr.addstr(self.header_size, 1, f"O diretório {self.current_path} está inacessível ou não existe.")

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

    def reset_configs(self):
        self.initial_path = False
        self.current_path = False
        self.options = []

    def go_back(self, interface):
        interface.stdscr.clear()

        if (self.current_path == self.initial_path):
            self.reset_configs()
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

    def print_header(self, interface):
        for idx, str_ in enumerate(self.header):
            interface.stdscr.addstr(idx, 1, str_)

    def render(self, interface):
        self.load_path(interface)
        self.print_header(interface)

        height, width = interface.stdscr.getmaxyx()
        visible_options = self.options[self.viewport_position:self.viewport_position+height-self.header_size]

        for i, option in enumerate(visible_options):
            option_index = self.viewport_position + i + 1

            if i == self.selected_option - self.viewport_position:
                interface.stdscr.addstr(i+self.header_size, 1, f"> {option_index}. {option}")
            else:
                interface.stdscr.addstr(i+self.header_size, 1, f"  {option_index}. {option}")

    def create_directory(self, interface):
        self.create_view.update_mode(CreateMode.DIRECTORY)
        self.create_view.set_path(self.current_path)

        interface.stdscr.clear()
        interface.current_view = self.create_view

    def create_file(self, interface):
        self.create_view.update_mode(CreateMode.FILE)
        self.create_view.set_path(self.current_path)

        interface.stdscr.clear()
        interface.current_view = self.create_view

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

        elif key == ord('\n'):
            self.choose_option(interface)

        elif 48 <= key <= 57:
            if int(chr(key)) in range(1, self.options_length + 1):
                self.selected_option = int(chr(key)) - 1
                self.choose_option(interface)
