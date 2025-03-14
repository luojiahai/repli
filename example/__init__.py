import repli
import repli.callback


def main():
    native_function = repli.callback.NativeFunction(function=lambda *args: print('command 1'))
    subprocess = repli.callback.Subprocess(arguments=lambda *args: 'echo command 2')
    commands = [
        repli.Command(name='1', description='command 1', callback=native_function),
        repli.Command(name='2', description='command 2', callback=subprocess),
    ]
    elements = [
        repli.Page(
            name='1',
            description='page 1',
            elements=commands,
        ),
    ]
    page = repli.Page(name='0', description='home', elements=elements)

    interpreter = repli.Interpreter(page=page)
    interpreter.loop()
