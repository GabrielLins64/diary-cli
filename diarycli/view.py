import abc
from abc import ABC, abstractmethod
import typing


class View(ABC):
    def __init__(self):
        self.__id: int = None
        self.__name: str = None
        self.__parent_id: int = None
        self.children: list[int] = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def parent(self):
        return self.__parent_id

    @parent.setter
    def parent(self, value):
        self.__parent_id = value

    @abstractmethod
    def render(self):
        pass
