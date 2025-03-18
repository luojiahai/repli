# 🐟 Read–Eval–Print Loop Interpreter (REPLI)

[![repli](https://img.shields.io/badge/🐟-repli-cyan?style=flat-square)](https://github.com/luojiahai/repli)
[![package](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-package.yml?style=flat-square&label=package&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-package.yml)
[![publish](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-publish.yml?style=flat-square&label=publish&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-publish.yml)
[![license](https://img.shields.io/github/license/luojiahai/repli?style=flat-square&logo=github&logoColor=white)](https://github.com/luojiahai/repli/blob/main/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/repli?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/repli?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/repli/)

It's a Python package for building command-line terminal applications.

Features:

- Breadcrumbs
- Interface panel
- Pagination

```
┌──────────────────────────────────────────────────────────────┐
│ [myapp] home                                                 │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 1  print hello world                                         │
│ 2  do something                                              │
│ 3  nested page                                               │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│ e  exit application  |  q  quit current page                 │
└──────────────────────────────────────────────────────────────┘
> 
```

## Install

```shell
pip install repli
```

## Usage

Example:

```python
page = Page(name="0", description="home")

@page.command(type=NativeFunction, name="1", description="print hello world")
def command_print_hello_world():
    print("hello world")

@page.command(type=Subprocess, name="2", description="do something")
def command_do_something():
    return "echo something else"

nested_page = Page(name="3", description="nested page")
page.add_page(page=nested_page)

interpreter = Interpreter(page=page, name="myapp")
interpreter.loop()
```

[Source](./example)

## Development

Requirements:

[Poetry](https://python-poetry.org/)

Setup environment:

```shell
poetry shell
poetry install
```

Run example application:

```shell
poetry run example
```

Type check:

```shell
poetry run mypy ./example ./repli ./tests
```

Format:

```shell
poetry run black ./example ./repli ./tests
```

Lint:

```shell
poetry run flake8 ./example ./repli ./tests --config ./.flake8
```

Test:

```shell
poetry run pytest
```

Coverage:

```shell
poetry run coverage run -m pytest &&
poetry run coverage report -m
```

Export `requirements.txt`:

```shell
poetry export --dev --without-hashes --format=requirements.txt > requirements.txt
```
