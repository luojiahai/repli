import interpreter
import readline
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text
from typing import Dict, List, Optional, Union


DEFAULT_PROMPT: str = '> '


class Interpreter:
    def __init__(
        self,
        prompt: str = DEFAULT_PROMPT,
        page: Optional[interpreter.Page] = None
    ) -> None:
        self._printer: interpreter.Printer = interpreter.Printer()
        self._prompt: str = prompt
        self._builtins: Dict[str, interpreter.Command] = {
            'e': self.command_exit('e'),
            'q': self.command_previous_page('q'),
        }
        self._pages: List[interpreter.Page] = [page]
        self._page_index: int = 0

    @property
    def printer(self) -> interpreter.Printer:
        return self._printer

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def builtins(self) -> Dict[str, interpreter.Command]:
        return self._builtins

    @property
    def pages(self) -> List[interpreter.Page]:
        return self._pages

    @property
    def page_index(self) -> int:
        return self._page_index

    @property
    def current_page(self) -> interpreter.Page:
        return self.pages[self.page_index]
    
    def print_breadcrumbs(self, pages: List[interpreter.Page], page_index: int) -> None:
        self.printer.print(Rule(style='dim cyan'))
        breadcrumbs: Text = Text(text='  ')
        for index, page in enumerate(pages):
            if index == page_index:
                breadcrumbs.append(f'{page.description}', style='bold underline')
            else:
                breadcrumbs.append(f'{page.description}')
            if index < len(pages) - 1:
                breadcrumbs.append(' > ')
        self.printer.print(breadcrumbs, style='cyan')
        self.printer.print(Rule(style='dim cyan'))

    def print_panel(self, title: str, commands: Dict[str, Union[interpreter.Command, interpreter.Page]]) -> None:
        table: Table = Table(
            highlight=False,
            show_header=False,
            expand=True,
            box='',
            show_lines=False,
            leading=0,
            border_style=None,
            row_styles=None,
            pad_edge=False,
            padding=(0, 1),
        )
        table.add_column('command', style='bold cyan', no_wrap=True)
        table.add_column('description', justify='left', no_wrap=False, ratio=10)
        for _, value in commands.items():
            table.add_row(value.name, value.description)

        panel: Panel = Panel(
            table,
            border_style='dim',
            title=title,
            title_align='left',
        )

        self.printer.print(panel)

    def command_exit(self, name: str) -> interpreter.Command:
        def exit() -> bool:
            self.printer.info('exited')
            return True
        return interpreter.Command(name=name, description='exit', callback=exit)

    def command_previous_page(self, name: str) -> interpreter.Command:
        def previous_page() -> bool:
            if self.page_index == 0:
                self.printer.error('no previous page')
                return False
            self._pages.pop()
            self._page_index -= 1
            return False
        return interpreter.Command(name=name, description='previous page', callback=previous_page)

    def execute(self, args: List[str]) -> bool:
        if not args:
            return False

        if args[0] in self.builtins:
            return self.builtins[args[0]]()

        if args[0] in self.current_page.dict:
            value: Optional[Union[interpreter.Command, interpreter.Page]] = self.current_page.dict.get(args[0])
            if isinstance(value, interpreter.Command):
                try:
                    return value.callback(*args[1:])
                except Exception as e:
                    self.printer.error(f'{e}')
            if isinstance(value, interpreter.Page):
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
            self.print_breadcrumbs(pages=self.pages, page_index=self.page_index)
            self.print_panel(title='commands', commands=self.current_page.dict)
            self.print_panel(title='builtins', commands=self.builtins)
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
