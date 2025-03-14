from repli import Command, Interpreter, Page
from repli.callback import NativeFunction, Subprocess


def main():
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
