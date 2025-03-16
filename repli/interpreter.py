import readline
from repli import console
from repli.command import Command, Page
from rich import box
from rich.padding import Padding
from rich.table import Table
from rich.text import Text
from typing import Dict, List, Optional, Union


DEFAULT_NAME: str = "[🐟]"
DEFAULT_PROMPT: str = ">"


class NoArgumentsError(Exception):
    pass


class Interpreter:
    def __init__(
        self,
        name: str = DEFAULT_NAME,
        prompt: str = DEFAULT_PROMPT,
        page: Optional[Page] = None,
    ) -> None:
        self._name: str = name
        self._prompt: str = prompt
        self._builtins: Dict[str, Command] = {
            "e": self.command_exit("e"),
            "q": self.command_quit("q"),
        }
        self._pages: List[Page] = [page]

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
    def current_page(self) -> Page:
        return self.pages[-1]

    def command_exit(self, name: str) -> Command:
        def exit() -> bool:
            console.info("exited")
            return True

        return Command(name=name, description="exit application", callback=exit)

    def command_quit(self, name: str) -> Command:
        def quit() -> bool:
            if len(self.pages) == 0:
                raise Exception("no pages to quit")
            if len(self.pages) == 1:
                raise Exception("current page is root page")
            self._pages.pop()
            return False

        return Command(name=name, description="quit current page", callback=quit)

    def header(self) -> Text:
        header: Text = Text(style="cyan")
        header.append(f"{self.name} ", style="bold")
        for index, page in enumerate(self.pages):
            if index == len(self.pages) - 1:
                header.append(f"{page.description}", style="bold underline")
            else:
                header.append(f"{page.description}")
            if index < len(self.pages) - 1:
                header.append(" > ")
        return header

    def panel(self) -> Table:
        table: Table = Table(
            show_header=False,
            expand=True,
            box=None,
            pad_edge=False,
        )
        table.add_column("name", style="bold cyan")
        table.add_column("description", justify="left", ratio=1)
        for _, value in self.current_page.commands.items():
            table.add_row(value.name, value.description)
        return table

    def footer(self) -> Text:
        footer: Text = Text()
        for key, value in self.builtins.items():
            footer.append(f"{value.name}", style="bold cyan")
            footer.append(f"  {value.description}")
            if key != list(self.builtins.keys())[-1]:
                footer.append("  |  ", style="dim")
        return footer

    def render(self) -> None:
        interface: Table = Table(
            box=box.SQUARE,
            expand=True,
            show_footer=True,
            header_style=None,
            footer_style=None,
            border_style="cyan",
        )
        interface.add_column(header=self.header(), footer=self.footer())
        interface.add_row(Padding(renderable=self.panel(), pad=(1, 0)))
        console.print(interface)

    def execute(self, args: List[str]) -> bool:
        if not args:
            raise NoArgumentsError("no arguments provided")

        result: Optional[bool] = None
        try:
            if args[0] in self.builtins:
                result = self.builtins[args[0]].callback()
            elif args[0] in self.current_page.commands:
                command: Optional[Union[Command, Page]] = (
                    self.current_page.commands.get(args[0])
                )
                if isinstance(command, Command):
                    result = command.callback(*args[1:])
                    console.input(prompt="press enter to continue")
                if isinstance(command, Page):
                    self._pages.append(command)
                    result = False
            else:
                raise Exception(f"command not found: {args[0]}")
        except Exception as e:
            console.error(f"{e}")
            console.input(prompt="press enter to continue")
        return result

    def loop(self, is_test: bool = False) -> None:
        line: Optional[str] = None
        args: Optional[str] = None
        status: bool = False

        while not status:
            console.clear()
            self.render()
            try:
                line = console.input(prompt=f"{self.prompt} ", markup=False)
                args = line.split()
                status = self.execute(args)
            except NoArgumentsError:
                status = False
            except EOFError:
                status = True
                console.print()
                console.info("exited with EOF")
            except KeyboardInterrupt:
                status = False
            finally:
                # break loop if testing
                if is_test:
                    break
