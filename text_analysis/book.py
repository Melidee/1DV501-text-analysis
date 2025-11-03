from io import TextIOWrapper
import os
from typing import Self


class GutenbergHeader:
    def __init__(self, file_path: str) -> None:
        title, author, release_date, language, credits = self.read_file(file_path)
        self.title: str = title
        self.author: str = author
        self.release_date: str = release_date
        self.language: str = language
        self.credits: str = credits

    def read_file(self, file_path: str) -> tuple[str, str, str, str, str]:
        with open(file_path, "r") as f:
            lines = f.readlines(1024)
        # hardcoded values for where certain metadata is, i.e title is always on line 11
        title = lines[11][7:]
        author = lines[13][9:]
        release_date = lines[15][14:]
        language = lines[18][10:]
        credits = lines[20][9:]
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

    def is_gutenburg(self) -> bool:
        with open(self.book_path, "r") as f:
            return f.read(32) == "﻿The Project Gutenberg eBook of "

    def gutenberg_header(self) -> GutenbergHeader | None:
        if self.is_gutenburg():
            return GutenbergHeader(self.book_path)
        else:
            return None

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
