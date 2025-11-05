import curses
from curses import KEY_UP, KEY_DOWN
import os
from os.path import isdir, isfile
from text_analysis.book import Book

KEY_ENTER = ord("\n")


def pick_book(win: curses.window, dir: str = ".") -> str:
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
    i, filename = prompt_selection(win, shown)
    if isdir(accessible[i][1]):
        return pick_book(win, os.path.join(dir + accessible[i][1]))
    return filename


def prompt_selection(
    win: curses.window, options: list[str], cursor: str = "➤ "
) -> tuple[int, str]:
    pad = " " * len(cursor)
    for i, option in enumerate(options):
        win.addstr(i, 0, f"{pad}{option}")
    win.refresh()
    hovering = 0
    while True:
        win.addstr(hovering, 0, f"{cursor}{options[hovering]}")
        win.refresh()
        key = win.getch()
        if key == KEY_UP:
            win.addstr(hovering, 0, f"{pad}{options[hovering]}")
            hovering = max(hovering - 1, 0)
        elif key == KEY_DOWN:
            win.addstr(hovering, 0, f"{pad}{options[hovering]}")
            hovering = min(hovering + 1, len(options))
        elif key == KEY_ENTER:
            win.clear()
            win.refresh()
            return hovering, options[hovering]

def show(win: curses.window, text: str) -> None:
    win.clear()
    lines = text.splitlines()
    for i, line in enumerate(text.splitlines()):
        win.addstr(i, 0, line)
    win.addstr(len(lines)+1, 0, "Press enter to continue...")
    win.refresh()
    _ = win.getch()
    win.clear()
    win.refresh()