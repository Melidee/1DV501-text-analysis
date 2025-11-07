import curses
import os
from curses import A_BOLD, KEY_UP, KEY_DOWN
from os.path import isfile
from typing import Callable
from text_analysis.book import Book
from string import ascii_letters, digits, punctuation, whitespace
from text_analysis.stats import Statistics


KEY_ENTER = ord("\n")


def pick_book(win: curses.window, dir: str = "./books") -> str:
    """Prompts the user to pick a book file from `dir`, returns the path to the chosen file"""
    file_names = [os.path.join(dir, name) for name in os.listdir(dir)]
    books = [Book(filename) for filename in file_names if isfile(filename)]

    book = prompt_selection(
        win,
        "Select a book to analyze",
        books,
        standard_view=Book.title,
        hover_view=Book.details,
    )
    return book.book_path


def prompt_selection[T](
    win: curses.window,
    title: str,
    options: list[T],
    cursor: str = "   ➤  ",
    standard_view: Callable[[T], str] = lambda e: str(e),
    hover_view: Callable[[T], str] = lambda e: str(e),
) -> T:
    """Prompt the user to pick from a set of options using their terminal arrow keys"""
    container = title_container(win, title)
    height, width = container.getmaxyx()
    container.addstr(height-1, 0, "Use arrow keys to move up and down, press Enter to select")

    views = [standard_view(option).ljust(width - len(cursor)) for option in options]
    hover_views = [hover_view(option) for option in options]
    pad = " " * len(cursor)

    for i, view in enumerate(views):
        container.addstr(i, 0, f"{pad}{view}")
    container.refresh()

    hovering = 0
    while True:
        container.addstr(hovering, 0, f"{cursor}{hover_views[hovering]}", A_BOLD)
        container.refresh()
        key = win.getch()
        if key == KEY_UP:
            container.addstr(hovering, 0, f"{pad}{views[hovering]}")
            hovering = max(hovering - 1, 0)
        elif key == KEY_DOWN:
            container.addstr(hovering, 0, f"{pad}{views[hovering]}")
            hovering = min(hovering + 1, len(options) - 1)
        elif key == KEY_ENTER:
            container.clear()
            container.refresh()
            return options[hovering]


def title_container(win: curses.window, title: str) -> curses.window:
    height, width = win.getmaxyx()
    title_win = curses.newwin(3, width)

    title_loc = (width - len(title)) // 2
    title_win.addstr(1, title_loc, title)

    subwin = curses.newwin(height - 4, width - 2, 3, 1)
    title_win.border()
    win.border()
    win.refresh()
    subwin.refresh()
    title_win.refresh()
    return subwin


def wrap_addstr(win: curses.window, y: int, x: int, text: str) -> int:
    """addstr to y, x, but with line wrapping"""
    height, width = win.getmaxyx()
    end_of_line = width - x
    first_chunk, text = text[:end_of_line], text[end_of_line:]
    win.addstr(y, x, first_chunk)
    offset = 1
    while text:
        chunk, text = text[:width], text[width:]
        line_y = y + offset
        if line_y > height:
            break
        win.addstr(line_y, x, chunk)
    return offset + 1


def show(win: curses.window, title: str, text: str) -> None:
    """Shows a body of text in the terminal with a title"""
    win.clear()
    container = title_container(win, title)
    height, _width = container.getmaxyx()
    i = 0
    for i, line in enumerate(text.splitlines()[:height]):
        _ = wrap_addstr(container, i, 0, line)
    container.refresh()
    _ = container.getch()
    win.clear()
    win.refresh()


def basic(stats: Statistics) -> str:
    return f"""  Lines: {stats.line_count()}
  Paragraphs: {stats.paragraph_count()}
  Sentences: {stats.sentence_count()}
  Words: {stats.total_word_count()}
  Unique Words: {stats.unique_word_count()}
  Characters: {stats.character_count()}
  Characters without whitespace: {stats.character_count(exclude_whitespace=True)}
  Average words per line: {stats.average_words_per_line()}
  Average word length: {stats.average_word_length()}
  Average words per sentence: {stats.average_words_per_sentence()}
{"─" * curses.COLS}"""


def word_analysis(stats: Statistics) -> str:
    text = ""
    for i, (word, count) in enumerate(stats.most_common_words()):
        word_percentage = count / stats.total_word_count() * 100
        text += (
            f"  {i + 1:>2}. {word:<20} {count:>6} times ({word_percentage:>4.1f}%)\n"
        )
    shortest_word = stats.shortest_word()
    longest_word = stats.longest_word()
    text += "\nWord length statistics:\n"
    text += f"  Shortest word: '{shortest_word}' ({len(shortest_word)} characters)\n"
    text += f"  Longest word: '{longest_word}' ({len(longest_word)} characters)\n"
    text += f"  Words appearing only once: {stats.words_only_once()}\n"
    text += "─" * curses.COLS
    return text


def sentence_analysis(stats: Statistics) -> str:
    avg_length = stats.total_word_count() / stats.sentence_count()
    shortest, shortest_len = stats.shortest_sentence()
    longest, longest_len = stats.longest_sentence()
    analysis = f"""Total sentences: {stats.sentence_count()}
Average words per sentence: {avg_length:.2f}
Shortest sentence: '{shortest}' ({shortest_len} words)
Longest sentence: '{longest}' ({longest_len} words)

Sentence length distribution (top 5):\n"""
    for length, count in stats.most_common_sentence_lengths():
        analysis += f"  {length} words: {count} sentences\n"
    analysis += "─" * curses.COLS
    return analysis


def character_analysis(stats: Statistics) -> str:
    letter_count = stats.char_kind_count(ascii_letters)
    digit_count = stats.char_kind_count(digits)
    whitespace_count = stats.char_kind_count(whitespace)
    punctuation_count = stats.char_kind_count(punctuation)
    char_count = stats.character_count()
    analysis = f"""Character type distribution:
  Letters: {letter_count} ({letter_count / char_count * 100:.1f}%)
  Digits: {digit_count} ({digit_count / char_count * 100:.1f}%)
  Spaces: {whitespace_count} ({whitespace_count / char_count * 100:.1f}%)
  Punctuation: {punctuation_count} ({punctuation_count / char_count * 100:.1f}%)

Most common letters:\n"""
    for i, (char, count) in enumerate(stats.most_common_letters()):
        percentage = count / letter_count * 100
        analysis += f"  {i}. '{char}' - {count} times ({percentage:.1f}%)\n"
    analysis += "─" * curses.COLS
    return analysis
