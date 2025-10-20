import os
from io import TextIOWrapper
from string import whitespace
from typing import Self

def main():
    print("Hello from text_analysis")
    book_path = "./alice-in-wonderland.txt"
    print(os.getcwd())
    with Book(book_path) as book:
        for word in book:
            print(word)

class Book:
    def __init__(self, book_path: str) -> None:
        self.book: TextIOWrapper = open(book_path, "r")
        self.tail: str = ""
        self.words: list[str] = []
        
    def read_chunk(self) -> None:
        words = self.tail + self.book.read(4096)
        if words and words[-1] not in whitespace:
            [words, *tail] = words.rsplit(maxsplit=1)
            self.tail = tail[0] if tail else ""
        self.words = words.split()
        
    def __iter__(self) -> Self:
        return self
        
    def __next__(self) -> str:
        if not self.words:
            self.read_chunk()
        if self.words:
            return self.words.pop(0)
        else:
            raise StopIteration
    
    def __enter__(self) -> Self:
        return self
        
    def __exit__(self, type: type, value, traceback) -> None:
        self.book.close()        

if __name__ == "__main__":
    main()