import json
from text_analysis.stats import Statistics


def basic(stats: Statistics) -> str:
    return f"""
Lines: {stats.line_count()}
Paragraphs: {stats.paragraph_count()}
Sentences: {stats.sentence_count()}
Words: {stats.total_word_count()}
Unique Words: {stats.unique_word_count()}
Characters: {stats.character_count()}
Characters without whitespace: {stats.character_count(exclude_whitespace=True)}
Average words per line: {stats.average_words_per_line()}
Average word length: {stats.average_word_length()}
Average words per sentence: {stats.average_words_per_sentence()}"""


def word_analysis(stats: Statistics) -> str:
    text = "Top 10 most common words:\n"
    for i, (word, count) in enumerate(stats.most_common_words()):
        word_percentage = count / stats.total_word_count() * 100
        text += (
            f"  {i + 1:>2}. {word:<20} {count:>6} times ({word_percentage:>4.1f}%)\n"
        )
    shortest_word = stats.shortest_word()
    longest_word = stats.longest_word()
    text += "\nWord length statistics:\n"
    text += f"  Shortest word: '{shortest_word}' ({len(shortest_word)} characters)\n"
    text += f"  Longest word: '{longest_word}' ({len(longest_word)} characters)\n"
    text += f"  Words appearing only once: {stats.words_only_once()}\n"
    return text


def sentence_analysis(stats: Statistics) -> str:
    avg_length = stats.total_word_count() / stats.sentence_count()
    shortest, shortest_len = stats.shortest_sentence()
    longest, longest_len = stats.longest_sentence()
    analysis = f"""
Total sentences: {stats.sentence_count()}
Average words per sentence: {avg_length}
Shortest sentence: '{shortest}' ({shortest_len} words)
Longest sentence: '{longest}' ({longest_len} words)

Sentence length distribution (top 5):\n"""
    for length, count in stats.most_common_sentence_lengths():
        analysis += f"  {length} words: {count} sentences\n"
    return analysis


def report(stats: Statistics) -> str:
    report = {
        "basic_statistics": {
            "lines": stats.line_count(),
            "paragraphs": stats.paragraph_count(),
            "sentences": stats.sentence_count(),
            "words": stats.total_word_count(),
            "unique_words": stats.unique_word_count(),
            "characters": stats.character_count(),
            "characters_without_whitespace": stats.character_count(
                exclude_whitespace=True
            ),
            "average_words_per_line": stats.average_words_per_line(),
            "average_word_length": stats.average_word_length(),
        },
        "word_analysis": {
            "most_common": [
                {"word": word, "count": count}
                for word, count in stats.most_common_words()
            ],
            "word_length_stats": {
                "shortest": stats.shortest_word(),
                "longest": stats.longest_word(),
                "average_length": stats.average_word_length(),
                "words_only_once": stats.words_only_once(),
            },
        },
    }
    return json.dumps(report)
