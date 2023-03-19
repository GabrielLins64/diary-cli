import abc
from abc import ABC, abstractmethod


class View(ABC):
    def __init__(self):
        self.__name: None
        self.__parent: View = None
        self.__shortcut: str = None
        self.children: list[type[View]] = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def shortcut(self):
        return self.__shortcut

    @shortcut.setter
    def shortcut(self, value: str):
        self.__shortcut = value

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass
