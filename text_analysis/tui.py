from readchar import readkey, key
from typing import Self
import os
from os.path import isdir, isfile
from text_analysis.book import Book

# ANSI escape code
ANSI_ESC = "\033"
KEY_UP = "\u0000H"


def pick_book(dir: str = ".") -> str:
    file_names = os.listdir(dir)
    file_paths = [os.path.join(dir, filename) for filename in file_names]
    file_pairs = list(zip(file_names, file_paths))
    dirs = [
        (name + "/", path)
        for name, path in file_pairs
        if isdir(path) and name[0] != "."
    ]
    gutenbergs = [
        (name, path)
        for name, path in file_pairs
        if isfile(path) and Book(path).is_gutenburg()
    ]  # strip hidden files
    accessible = dirs + gutenbergs
    shown = [name for name, _ in accessible]
    i, filename = prompt_selection(shown)
    with open("debug.txt", "w") as d:
        _ = d.write(f"{accessible}\n{i}")
    if isdir(accessible[i][1]):
        return pick_book(os.path.join(dir + accessible[i][1]))
    return filename


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
