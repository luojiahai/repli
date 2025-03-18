from pytest_mock import MockerFixture
from repli.command import Command, Page
from repli.interpreter import Interpreter, NoArgumentsError
from rich import box


def test_interpreter_init(mocker: MockerFixture):
    mock_page = mocker.MagicMock()
    mock_command_exit = mocker.patch("repli.interpreter.Interpreter.command_exit")
    mock_command_quit = mocker.patch("repli.interpreter.Interpreter.command_quit")

    interpreter = Interpreter(page=mock_page, name="name", prompt="prompt")

    assert interpreter.name == "name"
    assert interpreter.prompt == "prompt"
    assert interpreter.pages == [mock_page]
    assert interpreter.current_page == mock_page
    assert interpreter.builtins == {
        "e": mock_command_exit.return_value,
        "q": mock_command_quit.return_value,
    }
    mock_command_exit.assert_called_once_with("e")
    mock_command_quit.assert_called_once_with("q")


def test_interpreter_command_exit(mocker: MockerFixture):
    mock_console_info = mocker.patch("repli.console.Console.info")

    interpreter = Interpreter(page=mocker.MagicMock())
    command = interpreter.command_exit("test")
    result = command.callback()

    assert command.name == "test"
    assert command.description == "exit application"
    mock_console_info.assert_called_once_with("exited")
    assert result == True


def test_interpreter_command_quit(mocker: MockerFixture):
    interpreter = Interpreter(page=mocker.MagicMock())
    command = interpreter.command_quit("test")
    mocker.patch.object(interpreter, "_pages", [mocker.MagicMock(), mocker.MagicMock()])
    result = command.callback()

    assert command.name == "test"
    assert command.description == "quit current page"
    assert result == False


def test_interpreter_command_quit_no_pages(mocker: MockerFixture):
    interpreter = Interpreter(page=mocker.MagicMock())
    mocker.patch.object(interpreter, "_pages", [])
    command = interpreter.command_quit("test")

    try:
        command.callback()
    except Exception as e:
        assert str(e) == "no pages to quit"


def test_interpreter_command_quit_root_page(mocker: MockerFixture):
    interpreter = Interpreter(page=mocker.MagicMock())
    mocker.patch.object(interpreter, "_pages", [mocker.MagicMock()])
    command = interpreter.command_quit("test")

    try:
        command.callback()
    except Exception as e:
        assert str(e) == "current page is root page"


def test_interpreter_header(mocker: MockerFixture):
    mock_rich_text = mocker.patch("repli.interpreter.Text")
    spy_rich_text_append = mocker.spy(mock_rich_text.return_value, "append")

    interpreter = Interpreter(page=mocker.MagicMock())
    page_1 = Page(name="page_1", description="description_1")
    page_2 = Page(name="page_2", description="description_2")
    mocker.patch.object(interpreter, "_pages", [page_1, page_2])
    header = interpreter.header()

    assert header == mock_rich_text.return_value
    mock_rich_text.assert_called_once_with(style="cyan")
    spy_rich_text_append.assert_has_calls(
        [
            mocker.call(f"[{interpreter.name}] ", style="bold"),
            mocker.call(f"{page_1.description}"),
            mocker.call(" > "),
            mocker.call(f"{page_2.description}", style="bold underline"),
        ]
    )


def test_interpreter_panel(mocker: MockerFixture):
    mock_rich_table = mocker.patch("repli.interpreter.Table")
    spy_rich_table_add_column = mocker.spy(mock_rich_table.return_value, "add_column")
    spy_rich_table_add_row = mocker.spy(mock_rich_table.return_value, "add_row")

    interpreter = Interpreter(page=mocker.MagicMock())
    command = Command(
        name="test", description="description", callback=mocker.MagicMock()
    )
    page = Page(name="page", description="description")
    mocker.patch.object(page, "_commands", {command.name: command})
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


def test_interpreter_footer(mocker: MockerFixture):
    mock_rich_text = mocker.patch("repli.interpreter.Text")
    spy_rich_text_append = mocker.spy(mock_rich_text.return_value, "append")

    interpreter = Interpreter(page=mocker.MagicMock())
    command_1 = Command(
        name="test1", description="description", callback=mocker.MagicMock()
    )
    command_2 = Command(
        name="test2", description="description", callback=mocker.MagicMock()
    )
    builtins = {command_1.name: command_1, command_2.name: command_2}
    mocker.patch.object(interpreter, "_builtins", builtins)
    footer = interpreter.footer()

    assert footer == mock_rich_text.return_value
    mock_rich_text.assert_called_once_with()
    spy_rich_text_append.assert_has_calls(
        [
            mocker.call(f"{command_1.name}", style="bold cyan"),
            mocker.call(f"  {command_1.description}"),
            mocker.call("  |  ", style="dim"),
            mocker.call(f"{command_2.name}", style="bold cyan"),
            mocker.call(f"  {command_2.description}"),
        ]
    )


def test_interpreter_render(mocker: MockerFixture):
    mock_rich_table = mocker.patch("repli.interpreter.Table")
    spy_rich_table_add_column = mocker.spy(mock_rich_table.return_value, "add_column")
    spy_rich_table_add_row = mocker.spy(mock_rich_table.return_value, "add_row")
    mock_rich_padding = mocker.patch("repli.interpreter.Padding")
    mock_interpreter_header = mocker.patch("repli.interpreter.Interpreter.header")
    mock_interpreter_panel = mocker.patch("repli.interpreter.Interpreter.panel")
    mock_interpreter_footer = mocker.patch("repli.interpreter.Interpreter.footer")
    mock_console_print = mocker.patch("repli.console.Console.print")

    interpreter = Interpreter(page=mocker.MagicMock())
    interpreter.render()

    mock_rich_table.assert_called_once_with(
        box=box.SQUARE,
        expand=True,
        show_footer=True,
        header_style=None,
        footer_style=None,
        border_style="dim cyan",
    )
    spy_rich_table_add_column.assert_called_once_with(
        header=mock_interpreter_header.return_value,
        footer=mock_interpreter_footer.return_value,
    )
    spy_rich_table_add_row.assert_called_once_with(
        mock_rich_padding(renderable=mock_interpreter_panel.return_value, pad=(1, 0))
    )
    mock_console_print.assert_called_once_with(mock_rich_table.return_value)
    mock_interpreter_header.assert_called_once()
    mock_interpreter_panel.assert_called_once()
    mock_interpreter_footer.assert_called_once()


def test_interpreter_execute_no_args(mocker: MockerFixture):
    interpreter = Interpreter(page=mocker.MagicMock())

    try:
        interpreter.execute(args=[])
    except NoArgumentsError as e:
        assert str(e) == "no arguments provided"


def test_interpreter_execute_builtin_command(mocker: MockerFixture):
    mock_callback = mocker.MagicMock(return_value=False)

    interpreter = Interpreter(page=mocker.MagicMock())
    builtin_command = Command(
        name="test", description="description", callback=mock_callback
    )
    mocker.patch.object(interpreter, "_builtins", {"test": builtin_command})
    result = interpreter.execute(args=["test"])

    mock_callback.assert_called_once_with()
    assert result == False


def test_interpreter_execute_command(mocker: MockerFixture):
    mock_callback = mocker.MagicMock(return_value=False)
    mock_console_input = mocker.patch("repli.console.Console.input")

    command = Command(name="test", description="description", callback=mock_callback)
    page = Page(name="page", description="description")
    mocker.patch.object(page, "_commands", {command.name: command})
    interpreter = Interpreter(page=page)
    result = interpreter.execute(args=["test", "arg1", "arg2"])

    mock_callback.assert_called_once_with("arg1", "arg2")
    mock_console_input.assert_called_once_with(prompt="press enter to continue")
    assert result == False


def test_interpreter_execute_page(mocker: MockerFixture):
    nested_page = Page(name="test", description="description")
    page = Page(name="page", description="description")
    mocker.patch.object(page, "_commands", {nested_page.name: nested_page})
    interpreter = Interpreter(page=page)
    result = interpreter.execute(args=["test"])

    assert page in interpreter.pages
    assert result == False


def test_interpreter_execute_command_not_found(mocker: MockerFixture):
    mock_console_error = mocker.patch("repli.console.Console.error")
    mock_console_input = mocker.patch("repli.console.Console.input")

    page = Page(name="page", description="description")
    interpreter = Interpreter(page=page)
    interpreter.execute(args=["test"])

    mock_console_error.assert_called_once_with("command not found: test")
    mock_console_input.assert_called_once_with(prompt="press enter to continue")


def test_interpreter_loop(mocker: MockerFixture):
    mock_console_clear = mocker.patch("repli.console.Console.clear")
    mock_interpreter_render = mocker.patch("repli.interpreter.Interpreter.render")
    mock_console_input = mocker.patch(
        "repli.console.Console.input", return_value="test arg1 arg2"
    )
    mock_interpreter_execute = mocker.patch("repli.interpreter.Interpreter.execute")

    interpreter = Interpreter(page=mocker.MagicMock())
    interpreter.loop(is_test=True)

    mock_console_clear.assert_called_once()
    mock_interpreter_render.assert_called_once()
    mock_console_input.assert_called_once_with(
        prompt=f"{interpreter.prompt} ", markup=False
    )
    mock_interpreter_execute.assert_called_once_with(args=["test", "arg1", "arg2"])


def test_interpreter_loop_no_args(mocker: MockerFixture):
    mock_console_clear = mocker.patch("repli.console.Console.clear")
    mock_interpreter_render = mocker.patch("repli.interpreter.Interpreter.render")
    mock_console_input = mocker.patch("repli.console.Console.input", return_value="")
    mock_interpreter_execute = mocker.patch(
        "repli.interpreter.Interpreter.execute", side_effect=NoArgumentsError
    )

    interpreter = Interpreter(page=mocker.MagicMock())
    interpreter.loop(is_test=True)

    mock_console_clear.assert_called_once()
    mock_interpreter_render.assert_called_once()
    mock_console_input.assert_called_once_with(
        prompt=f"{interpreter.prompt} ", markup=False
    )
    mock_interpreter_execute.assert_called_once_with(args=[])


def test_interpreter_loop_eof(mocker: MockerFixture):
    mock_console_clear = mocker.patch("repli.console.Console.clear")
    mock_interpreter_render = mocker.patch("repli.interpreter.Interpreter.render")
    mock_console_input = mocker.patch(
        "repli.console.Console.input", side_effect=EOFError
    )
    mock_interpreter_execute = mocker.patch("repli.interpreter.Interpreter.execute")
    mock_console_print = mocker.patch("repli.console.Console.print")
    mock_console_info = mocker.patch("repli.console.Console.info")

    interpreter = Interpreter(page=mocker.MagicMock())
    interpreter.loop(is_test=True)

    mock_console_clear.assert_called_once()
    mock_interpreter_render.assert_called_once()
    mock_console_input.assert_called_once_with(
        prompt=f"{interpreter.prompt} ", markup=False
    )
    mock_interpreter_execute.assert_not_called()
    mock_console_print.assert_called_once_with()
    mock_console_info.assert_called_once_with("exited with EOF")


def test_interpreter_loop_keyboard_interrupt(mocker: MockerFixture):
    mock_console_clear = mocker.patch("repli.console.Console.clear")
    mock_interpreter_render = mocker.patch("repli.interpreter.Interpreter.render")
    mock_console_input = mocker.patch(
        "repli.console.Console.input", side_effect=KeyboardInterrupt
    )
    mock_interpreter_execute = mocker.patch("repli.interpreter.Interpreter.execute")

    interpreter = Interpreter(page=mocker.MagicMock())
    interpreter.loop(is_test=True)

    mock_console_clear.assert_called_once()
    mock_interpreter_render.assert_called_once()
    mock_console_input.assert_called_once_with(
        prompt=f"{interpreter.prompt} ", markup=False
    )
    mock_interpreter_execute.assert_not_called()
