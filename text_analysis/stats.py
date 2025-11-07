import random
from string import ascii_letters, digits, punctuation, whitespace
from typing import Any


class Statistics:
    """
    Aggregates and processes statistics for a given text.
    Data is added and processed in chunks.
    """

    def __init__(self) -> None:
        # this set is redundant, its the same as the keys of self.words
        self.words_set: set[str] = set()
        self.words: dict[str, int] = dict()
        self.chars: dict[str, int] = {
            " ": 0,
            "\t": 0,
            "\n": 0,
            ".": 0,
        }  # initialize characters that are literally referenced to avoid exceptions
        self.last_char: str = ""
        self.last_line: str = ""
        self.sentence_buf: str = ""
        self.sentences: dict[int, int] = {}
        self._sentence_shortest: str = "a " * 50  # very long sentence
        self._sentence_longest: str = ""
        self.paragraphs: int = 0
        self.lines: dict[int, int] = {}

    def analyze_chunk(self, lines: list[str]) -> None:
        for line in lines:
            line += "\n"  # preserve newline for character counting
            self._analyze_line(line)

    def _analyze_line(self, line: str) -> None:
        words_in_line = len(line.split())
        current_line_len_count = get_or_default(self.lines, words_in_line, 0)
        self.lines[words_in_line] = current_line_len_count + 1

        line_terminates_paragraph = line.strip() == "" and self.last_line.strip() != ""
        if line_terminates_paragraph:
            # end sentence on paragraph end
            self.add_sentence()
            self.paragraphs += 1

        word: str = ""
        for ch in line:
            if ch in ascii_letters + "'":
                word += ch
            else:
                if word:
                    words_in_line += 1
                    self._add_word(word)
                    word = ""
            self._add_char(ch)
        self.last_line = line

    def _add_word(self, word: str) -> None:
        """
        Adds a word to the statistics.
        Words are casefolded and apostrophes are included to ensure consistency
        """
        word = word.casefold()  # same words with different case are considered the same
        current_word_count = get_or_default(self.words, word, 0)
        self.words[word] = current_word_count + 1
        self.words_set.add(word)

    def _add_char(self, char: str) -> None:
        char_terminates_sentence = char == "." and self.last_char != char
        if char_terminates_sentence:
            self.add_sentence()
        else:
            self.sentence_buf += char

        current_char_count = get_or_default(self.chars, char, 0)
        self.chars[char] = current_char_count + 1

    # --- Line and paragraph methods --- #
    def add_sentence(self) -> None:
        # remove newlines so we can pretty print
        sentence = self.sentence_buf.replace("\n", " ")
        self.sentence_buf = ""

        word_count = len(sentence.split())
        if word_count == 0 or word_count == 1:
            return
        longest_word_count = len(self._sentence_longest.split())
        shortest_word_count = len(self._sentence_shortest.split())
        if word_count > longest_word_count:
            self._sentence_longest = sentence
        # random chance makes it more likely we get an interesting shortest sentence
        if word_count < shortest_word_count and random.randint(0, 10) == 0:
            self._sentence_shortest = sentence

        current_sentence_count = get_or_default(self.sentences, word_count, 0)
        self.sentences[word_count] = current_sentence_count + 1

    def line_count(self) -> int:
        return self.chars["\n"]

    def paragraph_count(self) -> int:
        return self.paragraphs

    def sentence_count(self) -> int:
        """Number of sentences within the text, a sentence is a string of words terminating in a `.`"""
        return sum(self.sentences.values())

    def average_words_per_line(self) -> float:
        total = 0
        for line_len, count in self.lines.items():
            total += line_len * count
        avg = total / sum(self.lines.values())
        return round(avg, 2)

    # --- Word methods --- #
    def unique_word_count(self) -> int:
        """Returns the number of unique words found within the text."""
        return len(self.words_set)

    def most_common_words(self, n: int = 10) -> list[tuple[str, int]]:
        """The most common `n` words found within the text, defaults to 10 words."""
        ordered_by_occurances = sorted(
            self.words.items(), key=lambda e: e[1], reverse=True
        )
        top_n_books = ordered_by_occurances[0:n]
        return top_n_books

    def average_word_length(self) -> float:
        total = 0
        for word, count in self.words.items():
            total += len(word) * count
        avg = total / self.total_word_count()
        return round(avg, 2)

    def total_word_count(self) -> int:
        """The total number of words found within the text."""
        return sum(self.words.values())

    def shortest_word(self) -> str:
        # sorted so 'a' is prioritized and it's unlikely to be an artifact
        return min(sorted(self.words.keys()), key=lambda w: len(w))

    def longest_word(self) -> str:
        return max(self.words.keys(), key=lambda w: len(w))

    def words_only_once(self) -> int:
        words_once = [word for word, count in self.words.items() if count == 1]
        return len(words_once)

    def word_lengths(self) -> list[tuple[int, int]]:
        return [(len(word), count) for word, count in self.words.items()]

    # --- Sentence methods --- #
    def average_words_per_sentence(self) -> float:
        total = 0
        for sentence_len, count in self.sentences.items():
            total += sentence_len * count
        avg = total / self.sentence_count()
        return round(avg, 2)

    def most_common_sentence_lengths(self, n: int = 5) -> list[tuple[int, int]]:
        return sorted(self.sentences.items(), key=lambda e: e[1], reverse=True)[:n]

    def sentence_lengths(self) -> list[int]:
        lengths: list[int] = []
        for i in range(100):
            lengths.append(get_or_default(self.sentences, i, 0))
        return lengths

    def longest_sentence(self) -> tuple[str, int]:
        return self._sentence_longest.strip(), len(self._sentence_longest.split())

    def shortest_sentence(self) -> tuple[str, int]:
        return self._sentence_shortest.strip(), len(self._sentence_shortest.split())

    # --- Character methods --- #
    def most_common_letters(self, n: int = 10) -> list[tuple[str, int]]:
        ordered_by_occurances = sorted(
            self.chars.items(), key=lambda e: e[1], reverse=True
        )
        letters = [
            (ch, count) for ch, count in ordered_by_occurances if ch in ascii_letters
        ]
        return letters[0:n]

    def character_count(self, exclude_whitespace: bool = False) -> int:
        """Number of total characters in the book."""
        if exclude_whitespace:
            whitespace_count = self.char_kind_count(whitespace)
            return sum(self.chars.values()) - whitespace_count
        else:
            return sum(self.chars.values())

    def char_kind_count(self, kind: str) -> int:
        total = 0
        for letter in kind:
            total += get_or_default(self.chars, letter, 0)
        return total

    def report(self) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        """Return a dict that summarizes the statistics of the book, can be used to serialize results"""
        report = {
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
            "word_analysis": {
                "most_common": [
                    {"word": word, "count": count}
                    for word, count in self.most_common_words()
                ],
                "word_length_stats": {
                    "shortest": self.shortest_word(),
                    "longest": self.longest_word(),
                    "average_length": self.average_word_length(),
                    "words_only_once": self.words_only_once(),
                },
            },
            "sentence_analysis": {
                "total_count": self.sentence_count(),
                "shortest": self.shortest_sentence()[0],
                "shortest_length": self.shortest_sentence()[1],
                "longest": self.longest_sentence()[0],
                "longest_length": self.longest_sentence()[1],
            },
            "character_analysis": {
                "letters": self.char_kind_count(ascii_letters),
                "digits": self.char_kind_count(digits),
                "whitespace": self.char_kind_count(whitespace),
                "punctuation": self.char_kind_count(punctuation),
                "most_common": [
                    {"letter": letter, "count": count}
                    for letter, count in self.most_common_letters()
                ],
            },
        }
        return report


def get_or_default[K, V](d: dict[K, V], key: K, default: V) -> V:
    """Attempts to retrieve value of `key` from `d`, returning `default` if it does not exist"""
    try:
        return d[key]
    except KeyError:
        return default
