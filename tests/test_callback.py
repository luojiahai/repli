from pytest_mock import MockerFixture
from repli.callback import Callback, NativeFunction, Subprocess


def test_callback_call(mocker: MockerFixture):
    mock_console_info = mocker.patch("repli.console.Console.info")
    mock_console_error = mocker.patch("repli.console.Console.error")

    callback = Callback()
    result = callback("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_console_info.assert_has_calls(
        [
            mocker.call("callback function args: ('arg1', 'arg2')"),
            mocker.call(
                "callback function kwargs: {'kwarg1': 'kwarg1', 'kwarg2': 'kwarg2'}"
            ),
        ]
    )
    mock_console_error.assert_not_called()
    assert result == False


def test_callback_native_function_init(mocker: MockerFixture):
    mock_callable = mocker.MagicMock()
    native_function = NativeFunction(callable=mock_callable)
    assert native_function.callable == mock_callable


def test_callback_native_function_call(mocker: MockerFixture):
    mock_callback_call = mocker.patch("repli.callback.Callback.__call__")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_rich_rule = mocker.patch("repli.callback.Rule")
    mock_callable = mocker.MagicMock()

    native_function = NativeFunction(callable=mock_callable)
    result = native_function("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_callback_call.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_print.assert_has_calls(
        [
            mocker.call(mock_rich_rule(style="magenta")),
            mocker.call(mock_rich_rule(style="magenta")),
        ]
    )
    mock_callable.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_error.assert_not_called()
    assert result == False


def test_callback_native_function_call_exception(mocker: MockerFixture):
    mock_callback_call = mocker.patch("repli.callback.Callback.__call__")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_rich_rule = mocker.patch("repli.callback.Rule")
    mock_callable = mocker.MagicMock(side_effect=Exception("test"))

    native_function = NativeFunction(callable=mock_callable)
    result = native_function("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_callback_call.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_print.assert_has_calls(
        [
            mocker.call(mock_rich_rule(style="magenta")),
        ]
    )
    mock_callable.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_error.assert_called_once_with(
        "native function raised an exception: test"
    )
    assert result == False


def test_callback_subprocess_init(mocker: MockerFixture):
    mock_callable = mocker.MagicMock()
    subprocess = Subprocess(callable=mock_callable)
    assert subprocess.callable == mock_callable


def test_callback_subprocess_call(mocker: MockerFixture):
    mock_callback_call = mocker.patch("repli.callback.Callback.__call__")
    mock_console_info = mocker.patch("repli.console.Console.info")
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_rich_rule = mocker.patch("repli.callback.Rule")
    mock_callable = mocker.MagicMock(return_value="test")
    mock_subprocess_call = mocker.patch("subprocess.call", return_value=False)
    mock_shlex_split = mocker.patch("shlex.split", return_value=["test"])

    subprocess = Subprocess(callable=mock_callable)
    result = subprocess("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_callback_call.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_info.assert_has_calls(
        [mocker.call("running subprocess command: 'test'")]
    )
    mock_console_print.assert_has_calls(
        [
            mocker.call(mock_rich_rule(style="magenta")),
            mocker.call(mock_rich_rule(style="magenta")),
        ]
    )
    mock_callable.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_subprocess_call.assert_called_once_with(
        args=["test"], text=True, encoding="utf-8"
    )
    mock_shlex_split.assert_called_once_with("test")
    mock_console_error.assert_not_called()
    assert result == False


def test_callback_subprocess_call_bad_return_code(mocker: MockerFixture):
    mock_callback_call = mocker.patch("repli.callback.Callback.__call__")
    mock_console_info = mocker.patch("repli.console.Console.info")
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_rich_rule = mocker.patch("repli.callback.Rule")
    mock_callable = mocker.MagicMock(return_value="test")
    mock_subprocess_call = mocker.patch("subprocess.call", return_value=1)
    mock_shlex_split = mocker.patch("shlex.split", return_value=["test"])

    subprocess = Subprocess(callable=mock_callable)
    result = subprocess("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_callback_call.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_info.assert_has_calls(
        [mocker.call("running subprocess command: 'test'")]
    )
    mock_console_print.assert_has_calls(
        [
            mocker.call(mock_rich_rule(style="magenta")),
            mocker.call(mock_rich_rule(style="magenta")),
        ]
    )
    mock_callable.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_subprocess_call.assert_called_once_with(
        args=["test"], text=True, encoding="utf-8"
    )
    mock_shlex_split.assert_called_once_with("test")
    mock_console_error.assert_called_once_with("subprocess returned an error code: 1")
    assert result == False


def test_callback_subprocess_call_exception(mocker: MockerFixture):
    mock_callback_call = mocker.patch("repli.callback.Callback.__call__")
    mock_console_info = mocker.patch("repli.console.Console.info")
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_rich_rule = mocker.patch("repli.callback.Rule")
    mock_callable = mocker.MagicMock(return_value="test")
    mock_subprocess_call = mocker.patch(
        "subprocess.call", side_effect=Exception("test")
    )
    mock_shlex_split = mocker.patch("shlex.split", return_value=["test"])

    subprocess = Subprocess(callable=mock_callable)
    result = subprocess("arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2")

    mock_callback_call.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_console_info.assert_has_calls(
        [mocker.call("running subprocess command: 'test'")]
    )
    mock_console_print.assert_has_calls(
        [
            mocker.call(mock_rich_rule(style="magenta")),
        ]
    )
    mock_callable.assert_called_once_with(
        "arg1", "arg2", kwarg1="kwarg1", kwarg2="kwarg2"
    )
    mock_subprocess_call.assert_called_once_with(
        args=["test"], text=True, encoding="utf-8"
    )
    mock_shlex_split.assert_called_once_with("test")
    mock_console_error.assert_called_once_with("subprocess raised an exception: test")
    assert result == False
