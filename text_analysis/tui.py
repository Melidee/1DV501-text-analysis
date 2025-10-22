from readchar import readkey, key
from typing import Self

# ANSI escape code
ANSI_ESC = "\033"


def prompt_selection(options: list[str], cursor: str = "➤ ") -> tuple[int, str]:
    def print_cursor(line: int, cursor: str):
        move_down(line)
        print(f"\r{cursor}\r", end="")
        move_up(line)

    with HideCursor():
        options = [""] + options
        pad = " " * len(cursor)
        print()
        for option in options:
            print(f"{pad}{option}")
        move_up(len(options))
        hovering: int = 0
        while True:
            print_cursor(hovering, cursor)
            match readkey():
                case key.UP:
                    print_cursor(hovering, pad)
                    hovering = 0 if hovering == 0 else hovering - 1
                case key.DOWN:
                    print_cursor(hovering, pad)
                    hovering = (
                        hovering if hovering == len(options) - 1 else hovering + 1
                    )
                case key.SPACE | key.ENTER:
                    break
                case _:
                    continue
    for _ in range(len(options) + 1):
        clear_line()
        move_down()
    move_up(len(options) + 1)
    return hovering, options[hovering]


def move_up(lines: int = 1) -> None:
    print(f"{ANSI_ESC}[{lines}A", end="")


def move_down(lines: int = 1):
    print(f"{ANSI_ESC}[{lines}B", end="")


def move_left(cols: int = 1):
    print(f"{ANSI_ESC}[{cols}D", end="")


def move_right(cols: int = 1):
    print(f"{ANSI_ESC}[{cols}C", end="")


def line_start():
    print("\r", end="")


def clear_line():
    print(f"{ANSI_ESC}[2K", end="")


def hide_cursor():
    print(f"{ANSI_ESC}[?25l", end="")


def show_cursor():
    print(f"{ANSI_ESC}[?25h", end="")


def get_position():
    print(f"{ANSI_ESC}[6n", end="")


class HideCursor:
    """
    HideCursor is a convenience class to use python's context manager for hiding and showing the terminal cursor

    ```py
    with HideCursor():
        # cursor is hidden here
        ...
    # but not here
    ```
    """

    def __init__(self) -> None:
        pass

    def __enter__(self) -> Self:
        hide_cursor()
        return self

    def __exit__(self, type: type, value, _traceback) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        show_cursor()
