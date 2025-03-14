from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.page import Page


page = Page(description='home')

@page.command(type=NativeFunction, name='1', description='command 1')
def command_1():
    print('command 1')

@page.command(type=Subprocess, name='2', description='command 2')
def command_2():
    return 'echo command 2'

def main():
    interpreter = Interpreter(page=page)
    interpreter.loop()

if __name__ == '__main__':
    main()
