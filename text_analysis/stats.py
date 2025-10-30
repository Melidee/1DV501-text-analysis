import json
from string import ascii_letters
from typing import override, Any


class Statistics(json.JSONEncoder):
    """
    Aggregates and processes statistics for a given text.
    Data is added and processed in chunks.
    """

    def __init__(self) -> None:
        super().__init__()
        self.words: dict[str, int] = dict()
        self.chars: dict[str, int] = {
            " ": 0,
            "\t": 0,
            "\n": 0,
            ".": 0,
        }  # initialize characters that are literally referenced to avoid exceptions

    def analyze_chunk(self, chunk: str) -> None:
        word: str = ""
        for ch in chunk:
            if ch in ascii_letters + "'":
                word += ch
            else:
                if word:
                    self.add_word(word)
                    word = ""
            self.add_char(ch)

    def add_word(self, word: str) -> None:
        """
        Adds a word to the statistics.
        Words are casefolded and apostrophes are included to ensure consistency
        """
        word = word.casefold()  # same words with different case are considered the same
        current_word_count = count if (count := self.words.get(word)) else 0
        self.words[word] = current_word_count + 1

    def add_char(self, char: str) -> None:
        current_char_count = count if (count := self.chars.get(char)) else 0
        self.chars[char] = current_char_count + 1

    def basic_stats(self) -> str:
        return f"""
Lines: {self.line_count()}
Paragraphs: {...}
Sentences: {self.sentence_count()}
Words: {self.total_word_count()}
Unique Words: {self.unique_word_count()}
Characters: {self.character_count()}
Characters without whitespace: {self.character_count(exclude_whitespace=True)}
Average words per line: {...}
Average word length: {self.average_word_length():.2f}
Average words per sentence: {...}"""

    def unique_word_count(self) -> int:
        """Returns the number of unique words found within the text."""
        return len(self.words.keys())

    def most_common_words(self, n: int = 10) -> list[tuple[str, int]]:
        """The most common `n` words found within the text, defaults to 10 words."""
        ordered_by_occurances = sorted(
            self.words.items(), key=lambda e: e[1], reverse=True
        )
        top_n_books = ordered_by_occurances[0:n]
        return top_n_books

    def line_count(self) -> int:
        return self.chars["\n"]

    def paragraph_count(self) -> int: ...

    def sentence_count(self) -> int:
        """Number of sentences within the text, a sentence is a string of words terminating in a `.`"""
        return self.chars["."]

    def character_count(self, exclude_whitespace: bool = False) -> int:
        """Number of total characters in the book."""
        if exclude_whitespace:
            whitespace_count = self.chars[" "] + self.chars["\t"] + self.chars["\n"]
            return sum(self.chars.values()) - whitespace_count
        else:
            return sum(self.chars.values())

    def average_words_per_line(self) -> float: ...

    def average_word_length(self) -> float:
        total = 0
        for word, count in self.words.items():
            total += len(word) * count
        return total / self.total_word_count()

    def total_word_count(self) -> int:
        """The total number of words found within the text."""
        return sum(self.words.values())

    def report(self) -> dict[str, Any]:
        return {
            "basic_statistics": {
                "lines": self.line_count(),
                "paragraphs": self.paragraph_count(),
                "sentences": self.sentence_count(),
                "words": self.total_word_count(),
                "unique_words": self.unique_word_count(),
                "characters": self.character_count(),
                "characters_without_whitespace": self.character_count(
                    exclude_whitespace=True
                ),
                "average_words_per_line": self.average_words_per_line(),
                "average_word_length": self.average_word_length(),
            },
        }
