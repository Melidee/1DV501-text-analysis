import os
from io import TextIOWrapper
from string import whitespace, ascii_letters
from typing import Self

from text_analysis import tui
from text_analysis.stats import Statistics
from text_analysis.tui import prompt_selection


def main():
    tui.Cursor.show()
    print("Hello from text_analysis")
    book_path = pick_book()
    with Book(book_path) as book:
        stats = Statistics()
        for chunk in book:
            stats.analyze_chunk(chunk)
        print(
            f"There are {stats.total_word_count()} total words and {stats.unique_word_count()} unique words in {book_path}"
        )


def pick_book() -> str:
    files = os.listdir()
    i, _file = prompt_selection(files)
    return files[i]


class Book:
    def __init__(self, book_path: str) -> None:
        self.book: TextIOWrapper = open(book_path, "r")
        self.tail: str = ""

    def read_chunk(self) -> str:
        words = self.book.read(1024)
        if not words:
            return ""
        while (ch := self.book.read(1)) and ch != whitespace:
            words += ch
        words += ch
        return "".join(
            ch for ch in words if ch in ascii_letters + whitespace
        )

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> str:
        if (chunk := self.read_chunk()):
            return chunk
        else:
            raise StopIteration

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type: type, value, traceback) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        self.book.close()


if __name__ == "__main__":
    main()
