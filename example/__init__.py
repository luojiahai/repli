from repli import Interpreter
from repli.callback import NativeFunction, Subprocess
from repli.page import Page


page = Page(description='home')

@page.command(type=NativeFunction, name='1', description='print hello world')
def command_1():
    print('hello world')

@page.command(type=Subprocess, name='2', description='print something else')
def command_2():
    return 'echo something else'

def main():
    interpreter = Interpreter(page=page)
    interpreter.loop()
    # import sys
    # from time import sleep
    # sys.stdout.write('hello world\n')
    # for count in range(100):
    #     sleep(0.1)
    #     sys.stdout.write(f'\r{count}')
    #     sys.stdout.flush()