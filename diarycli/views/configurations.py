from diarycli.view import View
import curses


class Configurations(View):
    def __init__(self):
        super().__init__()
        self.name = 'Configurações'
        self.children = []
        self.options = [child.name for child in self.children]
        self.options.append("Voltar")
        self.options_length = len(self.options)
        self.selected_option = 0

    def choose_option(self, interface):
        if (self.selected_option == self.options_length - 1):
            interface.go_back()

    def render(self, interface):
        interface.stdscr.addstr(0, 1, self.name)

        for i in range(self.options_length):
            if i == self.selected_option:
                interface.stdscr.addstr(i+2, 1, f"> {self.options[i]}")
            else:
                interface.stdscr.addstr(i+2, 1, f"  {self.options[i]}")

    def handle_events(self, interface):
        key = interface.stdscr.getch()

        if key == curses.KEY_UP:
            self.selected_option = (self.selected_option - 1) % self.options_length
        elif key == curses.KEY_DOWN:
            self.selected_option = (self.selected_option + 1) % self.options_length

        if key == ord('\n'):
            self.choose_option(interface)
