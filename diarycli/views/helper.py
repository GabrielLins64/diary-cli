from diarycli.view import View
from diarycli.constants import TEXT_HELP_PTBR
import curses


class Help(View):
    """Help view

    Displays all information about the application usage.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Ajuda'
        self.children = []
        self.current_row = 0
        self.max_y, self.max_x = 0, 0
        self.pad = None
        self.num_of_lines = 0

    def create_pad(self):
        self.num_of_lines = len(TEXT_HELP_PTBR) // (self.max_x - 4)
        self.num_of_lines += TEXT_HELP_PTBR.count('\n')

        self.pad = curses.newpad(self.num_of_lines, self.max_x - 4)
        self.pad.scrollok(True)
        self.pad.addstr(0, 0, TEXT_HELP_PTBR)
        self.pad.refresh(self.current_row, 0, 4, 2, self.max_y - 2, self.max_x - 2)

    def render(self, interface):
        new_max_y, new_max_x = interface.stdscr.getmaxyx()

        if new_max_x != self.max_x or new_max_y != self.max_y:
            self.max_x, self.max_y = new_max_x, new_max_y

            interface.stdscr.clear()
            interface.stdscr.addstr(0, 1, self.name)
            interface.stdscr.addstr(2, 2, "Pressione (Q) para voltar...")
            interface.stdscr.refresh()

            self.create_pad()

    def handle_events(self, interface):
        key = interface.stdscr.getch()

        if key == curses.KEY_UP:
            if (self.current_row > 0):
                self.current_row -= 1
                self.pad.refresh(self.current_row, 0, 4, 2, self.max_y - 2, self.max_x - 2)

        elif key == curses.KEY_DOWN:
            if (self.current_row < self.num_of_lines - 7):
                self.current_row += 1
                self.pad.refresh(self.current_row, 0, 4, 2, self.max_y - 2, self.max_x - 2)

        elif key == ord('q'):
            self.max_y, self.max_x = 0, 0
            interface.stdscr.clear()
            interface.go_back()
