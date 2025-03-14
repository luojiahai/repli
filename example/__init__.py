from repli import Interpreter, Page
from repli.callback import NativeFunction, Subprocess


page = Page(name='0', description='home')

@page.command(name='1', description='command 1', type=NativeFunction)
def command_1(*args) -> None:
    print('command 1')

@page.command(name='2', description='command 2', type=Subprocess)
def command_2(*args) -> str:
    return 'echo command 2'

interpreter = Interpreter(page=page)

def main():
    interpreter.loop()
