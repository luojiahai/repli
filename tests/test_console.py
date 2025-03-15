from repli import console
from repli.console import ERROR_PREFIX, INFO_PREFIX, PREFIX
from pytest_mock import MockerFixture


def test_printer_info(mocker: MockerFixture):
    console_print_mock = mocker.patch("repli.console.Console.print")
    console.info('message')
    console_print_mock.assert_called_with(f'{PREFIX} {INFO_PREFIX} message', style='magenta', markup=False)

def test_printer_error(mocker: MockerFixture):
    console_print_mock = mocker.patch("repli.console.Console.print")
    console.error('message')
    console_print_mock.assert_called_with(f'{PREFIX} {ERROR_PREFIX} message', style='yellow', markup=False)
