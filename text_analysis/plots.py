from string import ascii_letters, punctuation, whitespace
from tracemalloc import Statistic, StatisticDiff
from text_analysis.stats import Statistics
import matplotlib.pyplot as plt


def basic_stats(stats: Statistics) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    text_composition(stats, ax1)
    character_type_dist(stats, ax2)
    plt.show()


def text_composition(stats: Statistics, ax) -> None:
    x_labels = ["Lines", "Paragraphs", "Sentences", "Unique Words"]
    counts = [
        stats.line_count(),
        stats.paragraph_count(),
        stats.sentence_count(),
        stats.unique_word_count(),
    ]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(x_labels, counts, color=bar_colors)

    ax.set_ylabel("Occurances")
    ax.set_title("Text composition")


def character_type_dist(stats: Statistics, ax) -> None:
    labels = ("Letters", "Spaces", "Punctuation")
    sizes = [
        stats.char_kind_count(ascii_letters),
        stats.char_kind_count(whitespace),
        stats.char_kind_count(punctuation),
    ]
    ax.set_title("Character composition")
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")


def word_analysis(stats: Statistics) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    most_common_words(stats, ax1)
    word_length_distribution(stats, ax2)
    plt.show()


def most_common_words(stats: Statistics, ax) -> None:
    most_common = stats.most_common_words()
    x_labels = [word for word, _count in most_common]
    counts = [count for _word, count in most_common]
    bar_colors = ["tab:red"]

    ax.set_ylabel("Occurances")
    ax.set_title("Most Common Words")
    ax.bar(x_labels, counts, color=bar_colors)


def word_length_distribution(stats: Statistics, ax) -> None:
    most_common = stats.word_lengths()
    x_labels = [word for word, _count in most_common]
    counts = [count for _word, count in most_common]
    bar_colors = ["tab:blue"]

    ax.set_ylabel("Occurances")
    ax.set_title("Word length distribution")
    ax.bar(x_labels, counts, color=bar_colors)


def sentence_analysis(stats: Statistics) -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sentence_length_distribution(stats, ax1)
    common_sentence_lengths(stats, ax2)
    plt.show()


def sentence_length_distribution(stats: Statistics, ax) -> None:
    sentence_lengths = stats.sentence_lengths()
    x_labels = [length for length, _count in sentence_lengths]
    counts = [count for _length, count in sentence_lengths]
    bar_colors = ["tab:blue"]

    ax.set_ylabel("Occurances")
    ax.set_title("Sentence length distribution")
    ax.bar(x_labels, counts, color=bar_colors)


def common_sentence_lengths(stats: Statistics, ax) -> None:
    sentence_lengths = stats.sentence_lengths()
    most_common = sorted(sentence_lengths, key=lambda x: x[1])
    top_10 = most_common[:10]
    x_labels = [length for length, _count in top_10]
    counts = [count for _length, count in top_10]
    bar_colors = ["tab:green"]

    ax.set_ylabel("Occurances")
    ax.set_title("Sentence length distribution")
    ax.bar(x_labels, counts, color=bar_colors)
