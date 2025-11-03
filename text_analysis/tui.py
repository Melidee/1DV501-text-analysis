from readchar import readkey, key
from typing import Self

# ANSI escape code
ANSI_ESC = "\033"
KEY_UP = "\u0000H"


def prompt_selection(options: list[str], cursor: str = "➤ ") -> tuple[int, str]:
    def print_cursor(line: int, cursor: str):
        move_down(line)
        print(f"\r{cursor}\r", end="")
        move_up(line)

    pad = " " * len(cursor)
    for option in options:
        print(f"{pad}{option}")
    move_up(len(options) + 1)
    hovering = 1

    with HideCursor():
        while True:
            print_cursor(hovering, cursor)
            key_pressed = readkey()
            if key_pressed == key.UP:
                print_cursor(hovering, pad)
                hovering = 0 if hovering == 0 else hovering - 1
            if key_pressed == key.DOWN:
                print_cursor(hovering, pad)
                hovering = hovering if hovering == len(options) else hovering + 1
            if key_pressed in (key.ENTER, key.SPACE):
                break
    clear_lines(len(options))
    return hovering - 1, options[hovering - 1]


def ansi_print(code: str) -> None:
    print(f"{ANSI_ESC}{code}", end="")


def move_up(lines: int = 1) -> None:
    ansi_print(f"[{lines}A")


def move_down(lines: int = 1):
    ansi_print(f"[{lines}B")


def move_left(cols: int = 1):
    ansi_print(f"[{cols}D")


def move_right(cols: int = 1):
    ansi_print(f"[{cols}C")


def line_start():
    print("\r", end="")


def clear_line():
    ansi_print("[2K")


def clear_lines(n: int):
    for _ in range(n + 1):
        clear_line()
        move_down()
    move_up(n + 1)


def hide_cursor():
    ansi_print("[?25l")


def show_cursor():
    ansi_print("[?25h")


def get_position():
    ansi_print("[6n")


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
