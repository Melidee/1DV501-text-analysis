import os
from os import path
from os.path import isdir, isfile

from text_analysis.book import Book
from text_analysis.stats import Statistics
from text_analysis.tui import prompt_selection


def main():
    print("Pick a book to analyze")
    book_path = pick_book()
    with Book(book_path) as book:
        stats = Statistics()
        for chunk in book:
            stats.analyze_chunk(chunk)
    print(
        f"There are {stats.total_word_count()} total words and {stats.unique_word_count()} unique words in {book_path}"
    )


def pick_book(dir: str = ".") -> str:
    file_names = os.listdir(dir)
    file_paths = [os.path.join(dir, filename) for filename in file_names]
    file_pairs = list(zip(file_names, file_paths))
    dirs = [(name + "/", path) for name, path in file_pairs if isdir(path) and name[0] != '.']
    gutenbergs = [(name, path) for name, path in file_pairs if isfile(path) and Book(path).is_gutenburg()]  # strip hidden files
    accessible = dirs + gutenbergs
    print(accessible)
    shown = [name for name, _ in accessible]
    i, filename = prompt_selection(shown)
    print(f'accessible: {accessible[i]}')
    if isdir(accessible[i][1]):
        return pick_book(os.path.join(dir + accessible[i][1]))
    return filename


if __name__ == "__main__":
    main()
