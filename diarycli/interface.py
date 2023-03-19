import os
from diarycli.view import View
from diarycli.views.menu import Menu
import curses


class Interface:
    def __init__(self):
        self.current_view: View = Menu()
        self.parent_view: View = None
        self.stdscr = None

    def go_back(self):
        if (not self.parent_view):
            exit(0)
        else:
            self.current_view = self.parent_view
            self.parent_view = self.current_view.parent

    def main_loop(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.clear()

        while True:
            self.current_view.render(self)
            self.current_view.handle_events(self)

    def execute(self):
        curses.wrapper(self.main_loop)
