from pytest_mock import MockerFixture
from repli.command import Command, Page
from repli.interpreter import Interpreter


def test_interpreter_init(mocker: MockerFixture):
    mock_page = mocker.MagicMock()
    mock_command_exit_return_value = mocker.MagicMock()
    mock_command_quit_return_value = mocker.MagicMock()
    mock_command_exit = mocker.patch(
        "repli.interpreter.Interpreter.command_exit",
        return_value=mock_command_exit_return_value
    )
    mock_command_quit = mocker.patch(
        "repli.interpreter.Interpreter.command_quit",
        return_value=mock_command_quit_return_value
    )

    interpreter = Interpreter(name="name", prompt="prompt", page=mock_page)

    assert interpreter.name == "name"
    assert interpreter.prompt == "prompt"
    assert interpreter.pages == [mock_page]
    assert interpreter.current_page == mock_page
    assert interpreter.builtins == {
        "e": mock_command_exit_return_value,
        "q": mock_command_quit_return_value
    }
    mock_command_exit.assert_called_once_with("e")
    mock_command_quit.assert_called_once_with("q")


def test_interpreter_command_exit(mocker: MockerFixture):
    mock_console_info = mocker.patch("repli.console.Console.info")

    interpreter = Interpreter()
    command = interpreter.command_exit("test")
    result = command.callback()

    assert command.name == "test"
    assert command.description == "exit application"
    mock_console_info.assert_called_once_with("exited")
    assert result == True


def test_interpreter_command_quit(mocker: MockerFixture):
    interpreter = Interpreter()
    command = interpreter.command_quit("test")
    mocker.patch.object(interpreter, "_pages", [mocker.MagicMock(), mocker.MagicMock()])
    result = command.callback()

    assert command.name == "test"
    assert command.description == "quit current page"
    assert result == False


def test_interpreter_command_quit_no_pages(mocker: MockerFixture):
    interpreter = Interpreter()
    mocker.patch.object(interpreter, "_pages", [])
    command = interpreter.command_quit("test")

    try:
        command.callback()
    except Exception as e:
        assert str(e) == "no pages to quit"


def test_interpreter_command_quit_root_page(mocker: MockerFixture):
    interpreter = Interpreter()
    mocker.patch.object(interpreter, "_pages", [mocker.MagicMock()])
    command = interpreter.command_quit("test")

    try:
        command.callback()
    except Exception as e:
        assert str(e) == "current page is root page"


def test_interpreter_header(mocker: MockerFixture):
    mock_rich_text = mocker.patch("repli.interpreter.Text")
    spy_rich_text_append = mocker.spy(mock_rich_text.return_value, "append")

    interpreter = Interpreter()
    page_1 = Page(name="page_1", description="description_1", commands={})
    page_2 = Page(name="page_2", description="description_2", commands={})
    mocker.patch.object(interpreter, "_pages", [page_1, page_2])
    header = interpreter.header()

    assert header == mock_rich_text.return_value
    mock_rich_text.assert_called_once_with(style="cyan")
    spy_rich_text_append.assert_has_calls(
        [
            mocker.call(f"{interpreter.name} ", style="bold"),
            mocker.call(f"{page_1.description}"),
            mocker.call(" > "),
            mocker.call(f"{page_2.description}", style="bold underline"),
        ]
    )


def test_interpreter_panel(mocker: MockerFixture):
    mock_rich_table = mocker.patch("repli.interpreter.Table")
    spy_rich_table_add_column = mocker.spy(mock_rich_table.return_value, "add_column")
    spy_rich_table_add_row = mocker.spy(mock_rich_table.return_value, "add_row")

    interpreter = Interpreter()
    command = Command(name="test", description="description", callback=mocker.MagicMock())
    page = Page(name="page", description="description", commands={command.name: command})
    mocker.patch.object(interpreter, "_pages", [page])
    panel = interpreter.panel()

    assert panel == mock_rich_table.return_value
    mock_rich_table.assert_called_once_with(
        show_header=False,
        expand=True,
        box=None,
        pad_edge=False,
    )
    spy_rich_table_add_column.assert_has_calls(
        [
            mocker.call("name", style="bold cyan"),
            mocker.call("description", justify="left", ratio=1),
        ]
    )
    spy_rich_table_add_row.assert_called_once_with(command.name, command.description)
