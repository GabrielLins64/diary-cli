from abc import ABC, abstractmethod


class View(ABC):
    """View abstract class.

    It is initialized with a name, a parent, a shortcut character and
    a empty list of children Views.
    """
    def __init__(self):
        self.__name: None
        self.__parent: View = None
        self.children: list[type[View]] = []

    @property
    def name(self):
        """Name getter"""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Name setter"""
        self.__name = value

    @property
    def parent(self):
        """Parend getter"""
        return self.__parent

    @parent.setter
    def parent(self, value):
        """Parend setter"""
        self.__parent = value

    @abstractmethod
    def render(self):
        """Render method

        Implements the current view renderization on the terminal.
        """
        pass

    @abstractmethod
    def handle_events(self):
        """Events handler

        Handles I/O and other events.
        """
        pass
