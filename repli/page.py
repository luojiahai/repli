import repli
import repli.callback
from typing import Callable, Dict, Self, Type, Union


class Page:
    def __init__(self, name: str, description: str) -> None:
        self._name: str = name
        self._description: str = description
        self._commands: Dict[str, Union[repli.Command, Self]] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def commands(self) -> Dict[str, Union[repli.Command, Self]]:
        return self._commands

    def command(self, name: str, description: str, type: Type) -> Callable:
        def decorator(callable: Callable[[str, str], repli.Callback]) -> None:
            if type == repli.callback.NativeFunction:
                callback = repli.callback.NativeFunction(callable=callable)
            elif type == repli.callback.Subprocess:
                callback = repli.callback.Subprocess(callable=callable)
            else:
                raise ValueError('invalid callback type')
            command = repli.Command(name=name, description=description, callback=callback)
            self._commands[name] = command
        return decorator
