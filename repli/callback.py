import abc
import repli
import subprocess
import shlex
from typing import Callable


class Callback(abc.ABC):
    def __init__(self) -> None:
        pass

    def __call__(self, printer: repli.Printer, *args: str, **kwargs: str) -> bool:
        raise NotImplementedError


class NativeFunction(Callback):
    def __init__(
        self,
        function: Callable[[str, str], None],
    ) -> None:
        super().__init__()
        self._function: Callable[[str, str], None] = function

    @property
    def function(self) -> Callable[[str, str], None]:
        return self._function

    def __call__(self, printer: repli.Printer, *args: str, **kwargs: str) -> bool:
        printer.info(f'callback function args: {args}')
        printer.info(f'callback function kwargs: {kwargs}')
        try:
            printer.info('native function begin')
            self.function(*args, **kwargs)
            printer.info('native function end')
        except Exception as e:
            printer.error(f'native function raised an exception: {e}')
        finally:
            return False


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

    def __call__(self, printer: repli.Printer, *args: str, **kwargs: str) -> bool:
        printer.info(f'callback function args: {args}')
        printer.info(f'callback function kwargs: {kwargs}')
        arguments = self.arguments(*args, **kwargs)
        printer.info(f'running subprocess command: \'{arguments}\'')
        try:
            printer.info('subprocess begin')
            returncode = subprocess.call(
                args=shlex.split(arguments),
                text=True,
                encoding='utf-8',
            )
            printer.info('subprocess end')
            if returncode != 0:
                printer.error(f'subprocess returned an error code: {returncode}')
            else:
                printer.info('subprocess returned successfully')
        except Exception as e:
            printer.error(f'subprocess raised an exception: {e}')
        finally:
            return False
