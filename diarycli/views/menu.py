from diarycli.view import View
from diarycli.views import navigate, search, configurations, helper
import curses


class Menu(View):
    """Menu main view

    The first view available to user. Its only goal is to
    let user navigate through all main options.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Menu principal'
        self.children: list[View] = [
            search.Search(),
            navigate.Navigate(),
            configurations.Configurations(),
            helper.Help(),
        ]

        for child in self.children:
            child.parent = self

        self.options = [child.name for child in self.children]
        self.options.append("Sair")
        self.options_length = len(self.options)
        self.selected_option = 0

    def choose_option(self, interface):
        interface.stdscr.clear()

        if (self.selected_option == self.options_length - 1):
            interface.go_back()
        else:
            interface.current_view = self.children[self.selected_option]

    def render(self, interface):
        interface.stdscr.addstr(0, 1, self.name)

        for i in range(self.options_length):
            if i == self.selected_option:
                interface.stdscr.addstr(i+2, 1, f"> {i+1}. {self.options[i]}")
            else:
                interface.stdscr.addstr(i+2, 1, f"  {i+1}. {self.options[i]}")

        # interface.stdscr.addstr(self.options_length + 3, 1, f"itf m.a.: {hex(id(interface))}")
        # interface.stdscr.addstr(self.options_length + 4, 1, f"self m.a.: {hex(id(self))}")

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
