from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.command import Page


page = Page(name="0", description="home")


@page.command(type=NativeFunction, name="1", description="print hello world")
def command_print_hello_world():
    print("hello world")


@page.command(type=Subprocess, name="2", description="do something")
def command_do_something():
    return "echo something else"


nested_page = Page(name="3", description="nested page")
page.add_page(page=nested_page)


def main():
    interpreter = Interpreter(page=page, name="myapp")
    interpreter.loop()
