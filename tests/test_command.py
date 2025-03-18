from pytest_mock import MockerFixture
from repli.callback import NativeFunction
from repli.command import Command, Page
from repli.callback import Subprocess


def test_command_init(mocker: MockerFixture):
    mock_callback = mocker.MagicMock()
    command = Command(description="description", callback=mock_callback)

    assert command.description == "description"
    assert command.callback == mock_callback


def test_page_init(mocker: MockerFixture):
    mock_commands = mocker.MagicMock()
    page = Page(description="description")
    mocker.patch.object(page, "_commands", mock_commands)

    assert page.description == "description"
    assert page.commands == mock_commands
    assert page.index == 1


def test_page_command_native_function(mocker: MockerFixture):
    page = Page(description="description")
    mock_callable = mocker.MagicMock()
    decorator = page.command(NativeFunction, "test description")
    decorator(mock_callable)

    assert "1" in page.commands
    command = page.commands["1"]
    assert isinstance(command, Command)
    assert command.description == "test description"
    assert isinstance(command.callback, NativeFunction)
    assert command.callback.callable == mock_callable
    assert page.index == 2


def test_page_command_subprocess(mocker: MockerFixture):
    page = Page(description="description")
    mock_callable = mocker.MagicMock()
    decorator = page.command(Subprocess, "test description")
    decorator(mock_callable)

    assert "1" in page.commands
    command = page.commands["1"]
    assert isinstance(command, Command)
    assert command.description == "test description"
    assert isinstance(command.callback, Subprocess)
    assert command.callback.callable == mock_callable
    assert page.index == 2


def test_page_command_invalid_type(mocker: MockerFixture):
    page = Page(description="description")

    try:
        decorator = page.command(str, "test description")
        decorator(mocker.MagicMock())
    except ValueError as e:
        assert str(e) == "invalid callback type"


def test_page_add_page(mocker: MockerFixture):
    page = Page(description="description")
    mock_page = mocker.MagicMock()
    page.add_page(page=mock_page)

    assert "1" in page.commands
    assert page.commands["1"] == mock_page
    assert page.index == 2
