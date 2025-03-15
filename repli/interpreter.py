import readline
from repli.command import Command
from repli.page import Page
from repli.printer import Printer
from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from typing import Dict, List, Optional, Union


DEFAULT_NAME: str = '[🐟] '
DEFAULT_PROMPT: str = '> '


class Interpreter:
    def __init__(
        self,
        name: str = DEFAULT_NAME,
        prompt: str = DEFAULT_PROMPT,
        page: Optional[Page] = None
    ) -> None:
        self._printer: Printer = Printer()
        self._name: str = name
        self._prompt: str = prompt
        self._builtins: Dict[str, Command] = {
            'e': self.command_exit('e'),
            'q': self.command_previous_page('q'),
        }
        self._pages: List[Page] = [page]
        self._page_index: int = 0

    @property
    def printer(self) -> Printer:
        return self._printer
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def builtins(self) -> Dict[str, Command]:
        return self._builtins

    @property
    def pages(self) -> List[Page]:
        return self._pages

    @property
    def page_index(self) -> int:
        return self._page_index

    @property
    def current_page(self) -> Page:
        return self.pages[self.page_index]
    
    def print_interface(self) -> None:
        # header
        header: Text = Text(style='cyan')
        header.append(self.name, style='bold')
        for index, page in enumerate(self.pages):
            if index == self.page_index:
                header.append(f'{page.description}', style='bold underline')
            else:
                header.append(f'{page.description}')
            if index < len(self.pages) - 1:
                header.append(' > ')

        # panel
        table: Table = Table(
            highlight=False,
            show_header=False,
            expand=True,
            box=None,
            show_lines=False,
            leading=0,
            border_style=None,
            row_styles=None,
            pad_edge=False,
            # padding=(0, 1),
        )
        table.add_column('name', style='bold cyan', no_wrap=True)
        table.add_column('description', justify='left', no_wrap=False, ratio=10)
        for _, value in self.current_page.commands.items():
            table.add_row(value.name, value.description)

        # footer
        footer: Text = Text()
        for key, value in self.builtins.items():
            footer.append(f'{key}', style='bold cyan')
            footer.append(f'  {value.description}')
            if key != list(self.builtins.keys())[-1]:
                footer.append('  |  ', style='dim')

        # interface
        group: Group = Group(
            header,
            Rule(style='dim'),
            Panel(
                renderable=table,
                box=box.SIMPLE,
            ),
            Rule(style='dim'),
            footer,
        )
        interface: Panel = Panel(
            renderable=group,
            box=box.ROUNDED,
            border_style='dim cyan',
        )

        self.printer.print(interface)

    def command_exit(self, name: str) -> Command:
        def exit() -> bool:
            self.printer.info('exited')
            return True
        return Command(name=name, description='exit', callback=exit)

    def command_previous_page(self, name: str) -> Command:
        def previous_page() -> bool:
            if self.page_index == 0:
                self.printer.error('no previous page')
                return False
            self._pages.pop()
            self._page_index -= 1
            return False
        return Command(name=name, description='previous page', callback=previous_page)

    def execute(self, args: List[str]) -> bool:
        if not args:
            return False

        if args[0] in self.builtins:
            return self.builtins[args[0]].callback()

        if args[0] in self.current_page.commands:
            value: Optional[Union[Command, Page]] = self.current_page.commands.get(args[0])
            if isinstance(value, Command):
                try:
                    return value.callback(*args[1:])
                except Exception as e:
                    self.printer.error(f'{e}')
            if isinstance(value, Page):
                self._pages.append(value)
                self._page_index += 1
        else:
            self.printer.error(f'command not found: {args[0]}')

        return False

    def loop(self) -> None:
        line: Optional[str] = None
        args: Optional[str] = None
        status: bool = False

        while not status:
            self.print_interface()
            try:
                line = input(self.prompt)
                args = line.split()
                status = self.execute(args)
            except EOFError:
                status = True
                self.printer.print()
                self.printer.info('exited with EOF')
            except KeyboardInterrupt:
                status = False
                self.printer.print()
                self.printer.info('keyboard interrupted')
