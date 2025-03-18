from pytest_mock import MockerFixture
from repli.callback import NativeFunction
from repli.command import Command, Page
from repli.callback import Subprocess


def test_command_init(mocker: MockerFixture):
    mock_callback = mocker.MagicMock()
    command = Command(name="name", description="description", callback=mock_callback)

    assert command.name == "name"
    assert command.description == "description"
    assert command.callback == mock_callback


def test_page_init(mocker: MockerFixture):
    mock_commands = mocker.MagicMock()
    page = Page(name="name", description="description")
    mocker.patch.object(page, "_commands", mock_commands)

    assert page.name == "name"
    assert page.description == "description"
    assert page.commands == mock_commands


def test_page_validate_name_in_commands(mocker: MockerFixture):
    page = Page(name="name", description="description")
    mocker.patch.object(page, "_commands", {"name": mocker.MagicMock()})

    try:
        page.validate("name")
    except ValueError as e:
        assert str(e) == "page or command with name 'name' already exists in current page"


def test_page_validate_name_in_reserved_names(mocker: MockerFixture):
    page = Page(name="name", description="description")
    mocker.patch("repli.command.RESERVED_NAMES", ["test"])

    try:
        page.validate("test")
    except ValueError as e:
        assert str(e) == "page or command name 'test' is reserved"


def test_page_command_native_function(mocker: MockerFixture):
    page = Page(name="name", description="description")
    mock_callable = mocker.MagicMock()
    decorator = page.command(NativeFunction, "test_command", "test description")
    decorator(mock_callable)

    assert "test_command" in page.commands
    command = page.commands["test_command"]
    assert isinstance(command, Command)
    assert command.name == "test_command"
    assert command.description == "test description"
    assert isinstance(command.callback, NativeFunction)
    assert command.callback.callable == mock_callable


def test_page_command_subprocess(mocker: MockerFixture):
    page = Page(name="name", description="description")
    mock_callable = mocker.MagicMock()
    decorator = page.command(Subprocess, "test_command", "test description")
    decorator(mock_callable)

    assert "test_command" in page.commands
    command = page.commands["test_command"]
    assert isinstance(command, Command)
    assert command.name == "test_command"
    assert command.description == "test description"
    assert isinstance(command.callback, Subprocess)
    assert command.callback.callable == mock_callable


def test_page_command_invalid_type(mocker: MockerFixture):
    page = Page(name="name", description="description")

    try:
        decorator = page.command(str, "test_command", "test description")
        decorator(mocker.MagicMock())
    except ValueError as e:
        assert str(e) == "invalid callback type"


def test_page_add_page(mocker: MockerFixture):
    page = Page(name="name", description="description")
    mock_page = mocker.MagicMock()
    mocker.patch.object(mock_page, "name", "test")
    page.add_page(page=mock_page)

    assert "test" in page.commands
    assert page.commands["test"] == mock_page
