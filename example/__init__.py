from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.page import PageFactory


page = PageFactory()

@page.command(type=NativeFunction, name='1', description='print hello world')
def command_print_hello_world():
    print('hello world')

@page.command(type=Subprocess, name='2', description='do something')
def command_do_something():
    return 'echo something else'

def main():
    interpreter = Interpreter(page=page.get(name='example', description='example page'))
    interpreter.loop()
