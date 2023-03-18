from diarycli.view import View


class Menu(View):
    def __init__(self):
        super().__init__()
        self.name = 'Menu principal'
        self.children = [
            Search(),
            Navigate(),
            Configuration(),
            Help(),
        ]
        for child in self.children:
            child.parent = self

    def render(self, stdscr):
        for option in self.options:
            print(str(option['id']) + ' - ' + option['description'])


class Search(View):
    def __init__(self):
        super().__init__()
        self.name = 'Menu principal'

    def render(self, stdscr):
        pass

class Navigate(View):
    def __init__(self):
        super().__init__()
        self.name = 'Menu principal'

    def render(self, stdscr):
        pass

class Configuration(View):
    def __init__(self):
        super().__init__()

    def render(self, stdscr):
        pass

class Help(View):
    def __init__(self):
        super().__init__()

    def render(self, stdscr):
        pass

