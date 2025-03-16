from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.command import PageFactory


page_factory = PageFactory()


@page_factory.command(type=NativeFunction, name="1", description="print hello world")
def command_print_hello_world():
    print("hello world")


@page_factory.command(type=Subprocess, name="2", description="do something")
def command_do_something():
    return "echo something else"


def main():
    page = page_factory.get(name="example", description="example page")
    interpreter = Interpreter(page=page)
    interpreter.loop()
