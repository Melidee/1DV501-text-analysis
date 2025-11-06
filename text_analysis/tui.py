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
    filename = prompt_selection(win, "Select a book to analyze", shown)
    i = shown.index(filename)
    if isdir(accessible[i][1]):
        return pick_book(win, os.path.join(dir + accessible[i][1]))
    return filename


def prompt_selection(
    win: curses.window, title: str, options: list[str], cursor: str = "   ➤  "
) -> str:
    container = title_container(win, title)
    pad = " " * len(cursor)
    for i, option in enumerate(options):
        container.addstr(i, 0, f"{pad}{option}")
    container.refresh()
    hovering = 0
    while True:
        container.addstr(hovering, 0, f"{cursor}{options[hovering]}")
        container.refresh()
        key = win.getch()
        if key == KEY_UP:
            container.addstr(hovering, 0, f"{pad}{options[hovering]}")
            hovering = max(hovering - 1, 0)
        elif key == KEY_DOWN:
            container.addstr(hovering, 0, f"{pad}{options[hovering]}")
            hovering = min(hovering + 1, len(options)-1)
        elif key == KEY_ENTER:
            container.clear()
            container.refresh()
            return options[hovering]

def title_container(win: curses.window, title: str, footer: str = "") -> curses.window:
    height, width = win.getmaxyx()
    title_win = curses.newwin(3, width)
    
    title_loc = (width - len(title)) // 2
    title_win.addstr(1, title_loc, title)
    
    subwin = curses.newwin(height - 4, width-2, 3, 1)
    title_win.border()
    win.border()
    win.refresh()
    subwin.refresh()
    title_win.refresh()
    return subwin

def show(win: curses.window, title: str, text: str) -> None:
    win.clear()
    container = title_container(win, title)
    height, width = container.getmaxyx()
    i = 0
    for i, line in enumerate(text.splitlines()[:height]):
        container.addnstr(i, 0, line, width)
    container.refresh()
    _ = container.getch()
    win.clear()
    win.refresh()
