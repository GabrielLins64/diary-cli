from diarycli.view import View
from diarycli.views.menu import Menu
import curses


class Interface:
    """Application interface.

    Implements some generic methods shared by all views and also
    handles the views/terminal interface during the program execution.
    """

    def __init__(self):
        """Initializes the interface with the main view
        as the Menu() view."""

        self.current_view: View = Menu()
        self.stdscr = None

    def go_back(self):
        """Returns to the parent view. If there is no parent view,
        the application is terminated with return code 0."""

        if not self.current_view.parent:
            exit(0)
        else:
            self.current_view = self.current_view.parent
            self.stdscr.clear()
            self.stdscr.refresh()

    def main_loop(self, stdscr):
        """Application main loop.

        Parameters
        ----------
        stdscr : curses.window
        """

        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.clear()

        while True:
            self.current_view.render(self)
            self.current_view.handle_events(self)

    def execute(self):
        """Executes the application main loop wrapped by curses library."""
        curses.wrapper(self.main_loop)
