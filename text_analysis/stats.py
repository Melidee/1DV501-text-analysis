class Statistics:
    def __init__(self) -> None:
        self.words: dict[str, int] = dict()

    def add(self, word: str) -> None:
        current_word_count = count if (count := self.words.get(word)) else 0
        self.words[word] = current_word_count + 1

    def unique_word_count(self) -> int:
        return len(self.words.keys())

    def most_common_words(self, number: int = 10) -> list[tuple[str, int]]:
        ordered = sorted(self.words.items(), key=lambda e: e[1])
        return ordered[::-1][0:number]
