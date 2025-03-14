import interpreter
from typing import Dict, List, Self, Union


class Page:
    def __init__(self, name: str, description: str, elements: List[Union[interpreter.Command, Self]] = []) -> None:
        self._name: str = name
        self._description: str = description
        self._elements: List[Union[interpreter.Command, Self]] = elements
        self._dict: Dict[str, Union[interpreter.Command, Self]] = {element.name: element for element in elements}

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def elements(self) -> List[Union[interpreter.Command, Self]]:
        return self._elements

    @property
    def dict(self) -> Dict[str, Union[interpreter.Command, Self]]:
        return self._dict
