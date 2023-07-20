from diarycli.view import View
import curses
from diarycli import configs


class Configurations(View):
    """Configuration view

    Let user to configure the application details as the
    default tracked directory, deploy script and default
    text editor.
    """

    def __init__(self):
        super().__init__()
        self.name = 'Configurações'
        self.children = []
        self.configs = {}
        self.load_configs()

        self.options = [child.name for child in self.children]
        self.options.append('Armazenamento')
        self.options.append('Editor padrão')
        self.options.append('Arquivo de salt')
        self.options.append('Restaurar configurações padrões')
        self.options.append('Voltar')
        self.options_length = len(self.options)
        self.selected_option = 0

    def load_configs(self):
        self.configs = configs.load_configs()

    def update_config_view(self, interface, config_name: str, config_description: str, config_code: str):
        curses.echo()
        pad = curses.newpad(8, 80)

        pad.addstr(0, 1, config_name)
        pad.addstr(1, 1, config_description)
        pad.addstr(3, 1, f"Atual: {self.configs[config_code]}")
        pad.addstr(4, 1, f"Novo: ")
        pad.addstr(6, 1, f"Digite o novo valor da configuração ou deixe")
        pad.addstr(7, 1, f"em branco para manter o valor atual.")

        pad.refresh(0, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)

        interface.stdscr.move(4, 7)

        new_value = interface.stdscr.getstr().decode('utf-8')

        if (new_value != ''):
            self.configs = configs.update_configs({config_code: new_value})

        curses.noecho()
        interface.stdscr.clear()
        interface.stdscr.refresh()

    def choose_option(self, interface):
        if (self.selected_option == 0):
            self.update_config_view(interface,
                                    "Armazenamento",
                                    "O caminho onde os arquivos e pastas são armazenados.",
                                    "storage")

        if (self.selected_option == 1):
            self.update_config_view(interface,
                                    "Editor padrão",
                                    "O editor de texto padrão utilizado.",
                                    "editor")

        if (self.selected_option == 2):
            self.update_config_view(interface,
                                    "Arquivo de salt",
                                    "Arquivo com o salt usado na criptografia.",
                                    "saltLocation")

        if (self.selected_option == 3):
            self.configs = configs.restore_default()
        
        if (self.selected_option == self.options_length - 1):
            interface.go_back()

    def render(self, interface):
        interface.stdscr.addstr(0, 1, self.name)

        for i in range(self.options_length):
            if i == self.selected_option:
                interface.stdscr.addstr(i + 2, 1, f"> {i+1}. {self.options[i]}")
            else:
                interface.stdscr.addstr(i + 2, 1, f"  {i+1}. {self.options[i]}")

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
