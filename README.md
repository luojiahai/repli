# Read–Eval–Print Loop Interpreter (REPLI)

[![repli](https://img.shields.io/badge/🧃-repli-red?style=flat-square)](https://github.com/luojiahai/repli)
[![build](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-publish.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-publish.yml)
[![license](https://img.shields.io/github/license/luojiahai/repli?style=flat-square&logo=github&logoColor=white)](https://github.com/luojiahai/repli/blob/main/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/repli?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/repli?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/repli/)

This is a Python package for building REPL applications.

Features:

- Pagination
- Interface panel

```shell
────────────────────────────────────────────────────────────────
  home
────────────────────────────────────────────────────────────────
╭─ commands ───────────────────────────────────────────────────╮
│ 1  page 1                                                    │
│ 2  page 2                                                    │
╰──────────────────────────────────────────────────────────────╯
╭─ builtins ───────────────────────────────────────────────────╮
│ e  exit                                                      │
│ q  previous page                                             │
╰──────────────────────────────────────────────────────────────╯
> _
```

## Install

Pip:

```shell
pip install repli
```

Poetry:

```shell
poetry add repli
```

## Usage

```python
from repli import Command, Interpreter, Page
from repli.callback import NativeFunction, Subprocess

native_function = NativeFunction(function=lambda *args: print('command 1'))
subprocess = Subprocess(arguments=lambda *args: 'echo command 2')
commands = [
    Command(name='1', description='command 1', callback=native_function),
    Command(name='2', description='command 2', callback=subprocess),
]
elements = [
    Page(
        name='1',
        description='page 1',
        elements=commands,
    ),
]
page = Page(name='0', description='home', elements=elements)
interpreter = Interpreter(page=page)
interpreter.loop()
```

See [example](./example).
