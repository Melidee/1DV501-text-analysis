from io import TextIOWrapper
import os
from typing import Self


def is_gutenburg(file_path: str) -> bool:
    try:
        with open(file_path, "r") as f:
            return f.read(32) == "﻿The Project Gutenberg eBook of "
    except UnicodeDecodeError:
        return False


class GutenbergHeader:
    GUTENBURG_START_CHAR: str = "﻿"

    def __init__(self, file: TextIOWrapper) -> None:
        if file.read(1) != self.GUTENBURG_START_CHAR:
            title, author, release_date, language, credits = "", "", "", "", ""
        else:
            title, author, release_date, language, credits = self.read_file(file)
        self.title: str = title
        self.author: str = author
        self.release_date: str = release_date
        self.language: str = language
        self.credits: str = credits

    def read_file(self, file: TextIOWrapper) -> tuple[str, str, str, str, str]:
        lines: list[str] = []
        while (line := file.readline())[
            0:40
        ] != "*** START OF THE PROJECT GUTENBERG EBOOK":
            lines.append(line)

        # hardcoded values for where certain metadata is, i.e title is always on line 10
        title = lines[10][7:-1]
        author = lines[12][8:-1]
        release_date = lines[14][14:-1]
        language = lines[17][10:-1]
        credits = lines[19][9:-1]
        return title, author, release_date, language, credits


class Book:
    """
    Utility class for reading a book from a file.
    """

    CHUNK_SIZE: int = 8192  # 8kb

    def __init__(self, book_path: str) -> None:
        self.book_path: str = book_path
        self.book: TextIOWrapper = open(book_path, "r")
        self.file_size: int = os.path.getsize(book_path)
        self.gutenburg: GutenbergHeader = GutenbergHeader(self.book)

    def title(self) -> str:
        if self.gutenburg.title:
            return self.gutenburg.title
        return self.book_path

    def title_and_author(self) -> str:
        if self.gutenburg.title and self.gutenburg.author:
            return f"{self.gutenburg.title} by {self.gutenburg.author}"
        return self.title()

    def details(self) -> str:
        if is_gutenburg(self.book_path):
            return f"{self.title_and_author()} {self.size()} ({self.book_path})"
        return f"{self.book_path} {self.size()}"

    def size(self) -> str:
        """Size of the book file formatted to be pretty, such as 5.1MB or 3.0KB"""
        file_size = self.file_size
        for unit in ["B", "KB", "MB", "GB"]:
            if file_size < 1024:
                return f"{file_size:.1f} {unit}"
            file_size /= 1024
        raise ValueError("Book is too large")

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> list[str]:
        if lines := self.book.readlines(self.CHUNK_SIZE):
            return lines
        else:
            raise StopIteration

    def __enter__(self) -> Self:
        return self

    def __exit__(self, type: type, value, traceback) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
        self.book.close()
