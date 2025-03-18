from pytest_mock import MockerFixture
from repli.console import Console


def test_console_info(mocker: MockerFixture):
    mock_console_print = mocker.patch("repli.console.Console.print")

    console = Console()
    console.info("message")

    mock_console_print.assert_called_with("info: message", style="magenta", markup=False)


def test_console_error(mocker: MockerFixture):
    mock_console_print = mocker.patch("repli.console.Console.print")

    console = Console()
    console.error("message")

    mock_console_print.assert_called_with("error: message", style="yellow", markup=False)
