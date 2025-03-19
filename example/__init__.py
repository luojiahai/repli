from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.command import Page


page = Page("home")


@page.command(NativeFunction, "print hello world")
def command_print_hello_world():
    print("hello world")


@page.command(Subprocess, "do something")
def command_do_something():
    return "echo something else"


nested_page = Page("nested page")
page.add_page(nested_page)


def main():
    interpreter = Interpreter(page, "myapp")
    interpreter.loop()
