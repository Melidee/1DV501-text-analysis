import json
from string import ascii_letters, whitespace
from typing import Any


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
        self.last_char: str = ""
        self.sentence_buf: str = ""
        self.sentences: dict[int, int] = {}
        self.paragraphs: int = 0
        self.lines: dict[int, int] = {}

    def analyze_chunk(self, lines: list[str]) -> None:
        for line in lines:
            line += "\n"  # preserve newline for character counting
            self.analyze_line(line)

    def analyze_line(self, line: str) -> None:
        words_in_line = 0
        word: str = ""
        for ch in line:
            if ch in ascii_letters + "'":
                word += ch
            else:
                if word:
                    words_in_line += 1
                    self.add_word(word)
                    word = ""
            self.add_char(ch)
        current_line_len_count = get_or_default(self.lines, words_in_line, 0)
        self.lines[words_in_line] = current_line_len_count + 1

    def add_word(self, word: str) -> None:
        """
        Adds a word to the statistics.
        Words are casefolded and apostrophes are included to ensure consistency
        """
        word = word.casefold()  # same words with different case are considered the same
        current_word_count = get_or_default(self.words, word, 0)
        self.words[word] = current_word_count + 1

    def add_char(self, char: str) -> None:
        char_terminates_sentence = char == "." and self.last_char != char
        if char_terminates_sentence:
            sentence_len = len(self.sentence_buf.split())
            current_line_count = get_or_default(self.sentences, sentence_len, 0)
            self.sentences[sentence_len] = current_line_count + 1
            self.sentence_buf = ""
        else:
            self.sentence_buf += char

        char_terminates_paragraph = char == "\n" and self.last_char != char
        if char_terminates_paragraph:
            self.paragraphs += 1

        current_char_count = get_or_default(self.chars, char, 0)
        self.chars[char] = current_char_count + 1

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

    def paragraph_count(self) -> int:
        return self.paragraphs

    def sentence_count(self) -> int:
        """Number of sentences within the text, a sentence is a string of words terminating in a `.`"""
        return sum(self.sentences.values())

    def character_count(self, exclude_whitespace: bool = False) -> int:
        """Number of total characters in the book."""
        if exclude_whitespace:
            whitespace_count = self.chars[" "] + self.chars["\t"] + self.chars["\n"]
            return sum(self.chars.values()) - whitespace_count
        else:
            return sum(self.chars.values())

    def average_words_per_line(self) -> float:
        total = 0
        for line_len, count in self.lines.items():
            total += line_len * count
        avg = total / self.line_count()
        return round(avg, 2)

    def average_word_length(self) -> float:
        total = 0
        for word, count in self.words.items():
            total += len(word) * count
        avg = total / self.total_word_count()
        return round(avg, 2)

    def average_words_per_sentence(self) -> float:
        total = 0
        for sentence_len, count in self.sentences.items():
            total += sentence_len * count
        avg = total / self.sentence_count()
        return round(avg, 2)

    def total_word_count(self) -> int:
        """The total number of words found within the text."""
        return sum(self.words.values())

    def basic_stats(self) -> str:
        return f"""
Lines: {self.line_count()}
Paragraphs: {self.paragraph_count()}
Sentences: {self.sentence_count()}
Words: {self.total_word_count()}
Unique Words: {self.unique_word_count()}
Characters: {self.character_count()}
Characters without whitespace: {self.character_count(exclude_whitespace=True)}
Average words per line: {self.average_words_per_line()}
Average word length: {self.average_word_length()}
Average words per sentence: {self.average_words_per_sentence()}"""

    def report(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
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


def filter_alpha(s: str) -> str:
    filtered = ""
    for c in s:
        if c in ascii_letters or whitespace:
            filtered += c
    return filtered


def get_or_default[K, V](d: dict[K, V], key: K, default: V) -> V:
    try:
        return d[key]
    except KeyError:
        return default
