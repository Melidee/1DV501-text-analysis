from string import ascii_letters, punctuation, whitespace
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
    bar_labels = ["red", "blue", "_red", "orange"]
    bar_colors = ["tab:red", "tab:blue", "tab:red", "tab:orange"]

    ax.bar(x_labels, counts, label=bar_labels, color=bar_colors)

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
