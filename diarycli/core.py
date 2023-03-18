import os
from diarycli.view import View
from diarycli.default_views import Menu
import curses


class Interface:
    def __init__(self):
        self.current_view: View = Menu()
        self.parent_view: View = None

    def choose_option(self, option):
        if (option == len(self.current_view.options) - 1):
            self.go_back()

    def go_back(self):
        if (not self.parent_view):
            exit(0)
        else:
            self.current_view = self.parent_view
            self.parent_view = self.current_view.parent

    def main_loop(self, stdscr):
        stdscr.clear()
        curses.curs_set(0)
        selected_option = 0

        while True:
            options = self.current_view.options
            options_length = len(options)

            stdscr.addstr(0, 1, self.current_view.name)

            for i in range(options_length):
                if i == selected_option:
                    stdscr.addstr(i+2, 1, f"> {options[i]['description']}")
                else:
                    stdscr.addstr(i+2, 1, f"  {options[i]['description']}")

            key = stdscr.getch()

            if key == curses.KEY_UP:
                selected_option = (selected_option - 1) % options_length
            elif key == curses.KEY_DOWN:
                selected_option = (selected_option + 1) % options_length

            if key == ord('\n'):
                stdscr.clear()
                self.choose_option(selected_option)


    def render(self):
        curses.wrapper(self.main_loop)
