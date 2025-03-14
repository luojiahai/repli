import interpreter


class Command:
    def __init__(self, name: str, description: str, callback: interpreter.Callback) -> None:
        self._name: str = name
        self._description: str = description
        self._callback: interpreter.Callback = callback

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def callback(self) -> interpreter.Callback:
        return self._callback

    def __call__(self, *args: str, **kwargs: str) -> bool:
        return self.callback(*args, **kwargs)
