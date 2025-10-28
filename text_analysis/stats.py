from string import ascii_letters


class Statistics:
    """
    Aggregates and processes statistics for a given text. 
    Data is added and processed in chunks.
    """
    
    def __init__(self) -> None:
        self.words: dict[str, int] = dict()
        self.other_chars: dict[str, int] = dict()

    def analyze_chunk(self, chunk: str) -> None:
        word: str = ''
        for ch in chunk:
            if ch in ascii_letters + '\'':
                word += ch
            else:
                if word:
                    self.add_word(word)
                    word = ''
                self.add_special_char(ch)
                

    def add_word(self, word: str) -> None:
        """
        Adds a word to the statistics.
        Words are casefolded and apostrophes are ignored to ensure consistency
        """
        current_word_count = count if (count := self.words.get(word)) else 0
        self.words[word] = current_word_count + 1
        
    def add_special_char(self, char: str) -> None:
        current_char_count = count if (count := self.other_chars.get(char)) else 0
        self.words[char] = current_char_count + 1

    def unique_word_count(self) -> int:
        """
        Returns the number of unique words found within the text.
        """
        return len(self.words.keys())

    def most_common_words(self, n: int = 10) -> list[tuple[str, int]]:
        """
        The most common `n` words found within the text, defaults to 10 words.
        """
        ordered_by_occurances = sorted(self.words.items(), key=lambda e: e[1], reverse=True)
        top_n_books = ordered_by_occurances[0:n]
        return top_n_books
        
    def number_of_lines(self) -> int:
        return self.other_chars['\n']
        
    def number_of_sentences(self) -> int:
        """
        Number of sentences within the text, a sentence is a string of words terminating in a `.`
        """
        return self.other_chars['.']

    def total_word_count(self) -> int:
        """
        The total number of words found within the text.
        """
        return sum(self.words.values())
