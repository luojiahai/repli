from pytest_mock import MockerFixture
from repli.command import Command


def test_command_init(mocker: MockerFixture):
    mock_callback = mocker.MagicMock()
    command = Command(name='name', description='description', callback=mock_callback)
    assert command.name == 'name'
    assert command.description == 'description'
    assert command.callback == mock_callback
