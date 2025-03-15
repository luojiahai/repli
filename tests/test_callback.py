from pytest_mock import MockerFixture
from repli.callback import Callback, NativeFunction, Subprocess


def test_callback_call_mock(mocker: MockerFixture):
    console_info_mock = mocker.patch("repli.console.Console.info")
    console_error_mock = mocker.patch("repli.console.Console.error")

    callback = Callback()
    result = callback('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')

    console_info_mock.assert_has_calls([
        mocker.call('callback function args: (\'arg1\', \'arg2\')'),
        mocker.call('callback function kwargs: {\'kwarg1\': \'kwarg1\', \'kwarg2\': \'kwarg2\'}'),
    ])
    console_error_mock.assert_not_called()
    assert result == False

def test_callback_native_function_call(mocker: MockerFixture):
    callback_call_mock = mocker.patch("repli.callback.Callback.__call__")
    console_print_mock = mocker.patch("repli.console.Console.print")
    console_error_mock = mocker.patch("repli.console.Console.error")
    rich_rule_mock = mocker.patch("repli.callback.Rule")
    callable_mock = mocker.MagicMock()

    native_function = NativeFunction(callable=callable_mock)
    result = native_function('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')

    callback_call_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_print_mock.assert_has_calls([
        mocker.call(rich_rule_mock(style='magenta')),
        mocker.call(rich_rule_mock(style='magenta')),
    ])
    callable_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_error_mock.assert_not_called()
    assert result == False

def test_callback_native_function_call_exception(mocker: MockerFixture):
    callback_call_mock = mocker.patch("repli.callback.Callback.__call__")
    console_print_mock = mocker.patch("repli.console.Console.print")
    console_error_mock = mocker.patch("repli.console.Console.error")
    rich_rule_mock = mocker.patch("repli.callback.Rule")
    callable_mock = mocker.MagicMock()
    callable_mock.side_effect = Exception('test')

    native_function = NativeFunction(callable=callable_mock)
    result = native_function('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')

    callback_call_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_print_mock.assert_has_calls([
        mocker.call(rich_rule_mock(style='magenta')),
    ])
    callable_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_error_mock.assert_called_once_with('native function raised an exception: test')
    assert result == False

def test_callback_subprocess_call(mocker: MockerFixture):
    callback_call_mock = mocker.patch("repli.callback.Callback.__call__")
    console_info_mock = mocker.patch("repli.console.Console.info")
    console_error_mock = mocker.patch("repli.console.Console.error")
    console_print_mock = mocker.patch("repli.console.Console.print")
    rich_rule_mock = mocker.patch("repli.callback.Rule")
    callable_mock = mocker.MagicMock()
    callable_mock.return_value = 'test'
    subprocess_call_mock = mocker.patch("subprocess.call")
    subprocess_call_mock.return_value = False
    shlex_split_mock = mocker.patch("shlex.split")
    shlex_split_mock.return_value = ['test']

    subprocess = Subprocess(callable=callable_mock)
    result = subprocess('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')

    callback_call_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_info_mock.assert_has_calls([
        mocker.call('running subprocess command: \'test\'')
    ])
    console_print_mock.assert_has_calls([
        mocker.call(rich_rule_mock(style='magenta')),
        mocker.call(rich_rule_mock(style='magenta')),
    ])
    callable_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    subprocess_call_mock.assert_called_once_with(args=['test'], text=True, encoding='utf-8')
    shlex_split_mock.assert_called_once_with('test')
    console_error_mock.assert_not_called()
    assert result == False

def test_callback_subprocess_call_exception(mocker: MockerFixture):
    callback_call_mock = mocker.patch("repli.callback.Callback.__call__")
    console_info_mock = mocker.patch("repli.console.Console.info")
    console_error_mock = mocker.patch("repli.console.Console.error")
    console_print_mock = mocker.patch("repli.console.Console.print")
    rich_rule_mock = mocker.patch("repli.callback.Rule")
    callable_mock = mocker.MagicMock()
    callable_mock.return_value = 'test'
    subprocess_call_mock = mocker.patch("subprocess.call")
    subprocess_call_mock.side_effect = Exception('test')
    shlex_split_mock = mocker.patch("shlex.split")
    shlex_split_mock.return_value = ['test']

    subprocess = Subprocess(callable=callable_mock)
    result = subprocess('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')

    callback_call_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    console_info_mock.assert_has_calls([
        mocker.call('running subprocess command: \'test\'')
    ])
    console_print_mock.assert_has_calls([
        mocker.call(rich_rule_mock(style='magenta')),
    ])
    callable_mock.assert_called_once_with('arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
    subprocess_call_mock.assert_called_once_with(args=['test'], text=True, encoding='utf-8')
    shlex_split_mock.assert_called_once_with('test')
    console_error_mock.assert_called_once_with('subprocess raised an exception: test')
    assert result == False
