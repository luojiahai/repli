from rich.console import Console
from rich.markup import escape


PREFIX: str = '[repli]'
INFO_PREFIX: str = 'info:'
ERROR_PREFIX: str = 'error:'


class Printer(Console):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Printer, cls).__new__(cls)
        return cls._instance

    def info(self, message: str) -> None:
        self.print(f'{escape(PREFIX)} {escape(INFO_PREFIX)} {escape(message)}', style='magenta')

    def error(self, message: str) -> None:
        self.print(f'{escape(PREFIX)} {escape(ERROR_PREFIX)} {escape(message)}', style='yellow')
