from rich.console import Console


DEFAULT_PREFIX = '\[repli]'
DEFAULT_INFO_PREFIX: str = 'info:'
DEFAULT_ERROR_PREFIX: str = 'error:'


class Printer(Console):
    def __init__(
        self,
        prefix: str = DEFAULT_PREFIX,
        info_prefix: str = DEFAULT_INFO_PREFIX,
        error_prefix: str = DEFAULT_ERROR_PREFIX,
    ) -> None:
        super().__init__()
        self._prefix: str = prefix
        self._info_prefix: str = info_prefix
        self._error_prefix: str = error_prefix

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def info_prefix(self) -> str:
        return self._info_prefix

    @property
    def error_prefix(self) -> str:
        return self._error_prefix

    def info(self, message: str) -> None:
        self.print(f'{self.prefix} {self.info_prefix} {message}', style='magenta')

    def error(self, message: str) -> None:
        self.print(f'{self.prefix} {self.error_prefix} {message}', style='yellow')
