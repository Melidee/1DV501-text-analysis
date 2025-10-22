from string import ascii_letters


class Statistics:
    def __init__(self) -> None:
        self.words: dict[str, int] = dict()
        self.other_chars: dict[str, int] = dict()

    def analyze_chunk(self, chunk: str) -> None:
        word: str = "" 
        for ch in chunk:
            if ch in ascii_letters + '\'':
                word += ch
            else:
                if word:
                    self.add_word(word)
                    word = ""
                self.add_special_char(ch)
                

    def add_word(self, word: str) -> None:
        current_word_count = count if (count := self.words.get(word)) else 0
        self.words[word] = current_word_count + 1
        
    def add_special_char(self, char: str) -> None:
        current_char_count = count if (count := self.other_chars.get(char)) else 0
        self.words[char] = current_char_count + 1

    def unique_word_count(self) -> int:
        return len(self.words.keys())

    def most_common_words(self, number: int = 10) -> list[tuple[str, int]]:
        ordered_by_occurances = sorted(self.words.items(), key=lambda e: e[1])
        top_n_books = ordered_by_occurances[::-1][0:number]
        return top_n_books
        
    def number_of_lines(self) -> int:
        return self.other_chars['\n']
        
    def number_of_sentences(self) -> int:
        return self.other_chars['.']

    def total_word_count(self) -> int:
        return sum(self.words.values())
