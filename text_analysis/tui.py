from readchar import readkey, key
from typing import Self

# ANSI escape code
ANSI_ESC = "\033"


def prompt_selection(options: list[str], cursor: str = "➤ ") -> tuple[int, str]:
    with HideCursor():
        pad = " " * len(cursor)

        def select(line: int, cursor: str):
            Cursor.move_down(line)
            print(f"\r{cursor}\r", end="")
            Cursor.move_up(line)

        for option in options:
            print(f"{pad}{option}")
        Cursor.move_up(len(options)+1)
        hovering: int = 0
        while True:
            select(hovering, cursor)
            match readkey():
                case key.UP:
                    select(hovering, pad)
                    hovering = 0 if hovering == 0 else hovering - 1
                case key.DOWN:
                    select(hovering, pad)
                    hovering = (
                        hovering if hovering == len(options) else hovering + 1
                    )
                case key.SPACE | key.ENTER:
                    return hovering, options[hovering]
                case _:
                    continue


class Cursor:
    @staticmethod
    def move_up(lines: int = 1) -> None:
        print(f"{ANSI_ESC}[{lines}A", end="")

    @staticmethod
    def move_down(lines: int = 1):
        print(f"{ANSI_ESC}[{lines}B", end="")

    @staticmethod
    def move_left(cols: int = 1):
        print(f"{ANSI_ESC}[{cols}C", end="")

    @staticmethod
    def move_right(cols: int = 1):
        print(f"{ANSI_ESC}[{cols}D", end="")

    @staticmethod
    def line_start():
        print("\r", end="")

    @staticmethod
    def hide():
        print(f"{ANSI_ESC}[?25l", end="")

    @staticmethod
    def show():
        print(f"{ANSI_ESC}[?25h", end="")

    @staticmethod
    def save_position():
        print(f"{ANSI_ESC}[s", end="")

    @staticmethod
    def load_position():
        print(f"{ANSI_ESC}[u", end="")


class HideCursor:
    def __init__(self) -> None:
        pass

    def __enter__(self) -> Self:
        Cursor.hide()
        return self

    def __exit__(self, type: type, value, _traceback) -> None: # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        Cursor.show()
