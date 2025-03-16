from pytest_mock import MockerFixture
from repli import console
from repli.console import ERROR_PREFIX, INFO_PREFIX, PREFIX


def test_console_info(mocker: MockerFixture):
    mock_console_print = mocker.patch("repli.console.Console.print")
    console.info('message')
    mock_console_print.assert_called_with(f'{PREFIX} {INFO_PREFIX} message', style='magenta', markup=False)


def test_console_error(mocker: MockerFixture):
    mock_console_print = mocker.patch("repli.console.Console.print")
    console.error('message')
    mock_console_print.assert_called_with(f'{PREFIX} {ERROR_PREFIX} message', style='yellow', markup=False)
