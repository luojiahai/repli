from pytest_mock import MockerFixture
from repli.callback import NativeFunction
from repli.command import Command, Page, PageFactory
from repli.callback import Subprocess


def test_command_init(mocker: MockerFixture):
    mock_callback = mocker.MagicMock()
    command = Command(name='name', description='description', callback=mock_callback)
    assert command.name == 'name'
    assert command.description == 'description'
    assert command.callback == mock_callback


def test_page_init(mocker: MockerFixture):
    mock_commands = mocker.MagicMock()
    page = Page(name='name', description='description', commands=mock_commands)
    assert page.name == 'name'
    assert page.description == 'description'
    assert page.commands == mock_commands


def test_page_factory_init():
    page_factory = PageFactory()
    assert page_factory.commands == {}


def test_page_factory_validate_name_in_commands(mocker: MockerFixture):
    page_factory = PageFactory()
    mocker.patch.object(page_factory, '_commands', {'name': mocker.MagicMock()})
    try:
        page_factory.validate('name')
    except ValueError as e:
        assert str(e) == 'page or command with name \'name\' already exists in current page'


def test_page_factory_validate_name_in_reserved_names(mocker: MockerFixture):
    page_factory = PageFactory()
    mocker.patch('repli.command.RESERVED_NAMES', ['test'])
    try:
        page_factory.validate('test')
    except ValueError as e:
        assert str(e) == 'page or command name \'test\' is reserved'


def test_page_factory_command_native_function(mocker: MockerFixture):
    page_factory = PageFactory()
    mock_callable = mocker.MagicMock()
    decorator = page_factory.command(NativeFunction, 'test_command', 'test description')
    decorator(mock_callable)

    assert 'test_command' in page_factory.commands
    command = page_factory.commands['test_command']
    assert isinstance(command, Command)
    assert command.name == 'test_command'
    assert command.description == 'test description'
    assert isinstance(command.callback, NativeFunction)
    assert command.callback.callable == mock_callable


def test_page_factory_command_subprocess(mocker: MockerFixture):
    page_factory = PageFactory()
    mock_callable = mocker.MagicMock()
    decorator = page_factory.command(Subprocess, 'test_command', 'test description')
    decorator(mock_callable)

    assert 'test_command' in page_factory.commands
    command = page_factory.commands['test_command']
    assert isinstance(command, Command)
    assert command.name == 'test_command'
    assert command.description == 'test description'
    assert isinstance(command.callback, Subprocess)
    assert command.callback.callable == mock_callable


def test_page_factory_command_invalid_type(mocker: MockerFixture):
    page_factory = PageFactory()
    try:
        decorator = page_factory.command(str, 'test_command', 'test description')
        decorator(mocker.MagicMock())
    except ValueError as e:
        assert str(e) == 'invalid callback type'


def test_page_factory_get(mocker: MockerFixture):
    page_factory = PageFactory()
    mocker.patch.object(page_factory, '_commands', {'test': mocker.MagicMock()})
    page = page_factory.get('test', 'test description')
    assert page.name == 'test'
    assert page.description == 'test description'
    assert page.commands == page.commands
