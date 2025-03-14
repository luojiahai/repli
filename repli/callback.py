import abc
import repli
import subprocess
import shlex
from typing import Callable


class Callback(abc.ABC):
    def __init__(self) -> None:
        self._printer = repli.Printer()

    @property
    def printer(self) -> repli.Printer:
        return self._printer

    def __call__(self, *args: str, **kwargs: str) -> bool:
        raise NotImplementedError


class Subprocess(Callback):
    def __init__(
        self,
        arguments: Callable[[str, str], str],
    ) -> None:
        super().__init__()
        self._arguments: Callable[[str, str], str] = arguments

    @property
    def arguments(self) -> Callable[[str, str], str]:
        return self._arguments

    def __call__(self, *args: str, **kwargs: str) -> bool:
        self.printer.info(f'callback function args: {args}')
        self.printer.info(f'callback function kwargs: {kwargs}')
        arguments = self.arguments(*args, **kwargs)
        self.printer.info(f'running subprocess command: \'{arguments}\'')
        try:
            self.printer.info('subprocess begin')
            returncode = subprocess.call(
                args=shlex.split(arguments),
                text=True,
                encoding='utf-8',
            )
            self.printer.info('subprocess end')
            if returncode != 0:
                self.printer.error(f'subprocess returned an error code: {returncode}')
            else:
                self.printer.info('subprocess returned successfully')
        except Exception as e:
            self.printer.error(f'subprocess raised an exception: {e}')
        finally:
            return False
