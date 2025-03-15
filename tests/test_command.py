from repli.command import Command
from pytest_mock import MockerFixture


def test_command(mocker: MockerFixture):
    mock_callback = mocker.MagicMock()
    command = Command(name='name', description='description', callback=mock_callback)
    assert command.name == 'name'
    assert command.description == 'description'
    assert command.callback == mock_callback
