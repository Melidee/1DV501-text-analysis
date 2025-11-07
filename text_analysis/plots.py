import datetime
import os
from string import ascii_letters, punctuation, whitespace
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from text_analysis.book import Book
from text_analysis.stats import Statistics
import matplotlib.pyplot as plt


def show_plot(analysis_kind: str, stats: Statistics, book: Book) -> str:
    if analysis_kind == "Basic Analysis":
        fig = basic_stats(stats)
    elif analysis_kind == "Word Analysis":
        fig = word_analysis(stats)
    elif analysis_kind == "Sentence Analysis":
        fig = sentence_analysis(stats)
    elif analysis_kind == "Character Analysis":
        fig = character_analysis(stats)
    else:
        raise ValueError("unknown analysis type")
    timestamp = datetime.datetime.now().strftime("%m-%d %H:%M")
    filename = f"plots/{analysis_kind} {timestamp}.png"
    fig.suptitle(f"{analysis_kind} for {book.title()}")
    fig.tight_layout()
    os.makedirs(os.path.dirname("./plots/"), exist_ok=True)
    fig.savefig(filename)
    return filename


def basic_stats(stats: Statistics) -> Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    text_composition(stats, ax1)
    character_type_dist(stats, ax2)
    return fig


def text_composition(stats: Statistics, ax: Axes) -> None:
    x_labels = ["Lines", "Paragraphs", "Sentences", "Unique Words"]
    counts = [
        stats.line_count(),
        stats.paragraph_count(),
        stats.sentence_count(),
        stats.unique_word_count(),
    ]
    bar_colors = ["tab:red", "tab:blue", "tab:green", "tab:orange"]

    ax.bar(x_labels, counts, color=bar_colors)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_xlabel("Words")
    ax.set_ylabel("Occurances")
    ax.set_title("Text composition")


def character_type_dist(stats: Statistics, ax: Axes) -> None:
    labels = ("Letters", "Spaces", "Punctuation")
    sizes = [
        stats.char_kind_count(ascii_letters),
        stats.char_kind_count(whitespace),
        stats.char_kind_count(punctuation),
    ]
    ax.set_title("Character composition")
    ax.pie(sizes, labels=labels, autopct="%1.1f%%")


def word_analysis(stats: Statistics) -> Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    most_common_words(stats, ax1)
    word_length_distribution(stats, ax2)
    return fig


def most_common_words(stats: Statistics, ax) -> None:
    most_common = stats.most_common_words()
    x_labels = [word for word, _count in most_common]
    counts = [count for _word, count in most_common]
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_ylabel("Occurances")
    ax.set_title("Most Common Words")
    ax.bar(x_labels, counts, color="tab:red")


def word_length_distribution(stats: Statistics, ax: Axes) -> None:
    most_common = stats.word_lengths()
    x_labels = [word for word, _count in most_common]
    counts = [count for _word, count in most_common]
    bar_colors = ["tab:blue"]

    ax.set_ylabel("Occurances")
    ax.set_title("Word length distribution")
    ax.bar(x_labels, counts, color=bar_colors)


def sentence_analysis(stats: Statistics) -> Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    sentence_length_distribution(stats, ax1)
    common_sentence_lengths(stats, ax2)
    return fig


def sentence_length_distribution(stats: Statistics, ax: Axes) -> None:
    sentence_lengths = stats.sentence_lengths()
    ax.set_xlabel("Sentence length (words)")
    ax.set_ylabel("Occurances")
    ax.set_title("Sentence length distribution")
    ax.hist(sentence_lengths, bins=10, color="tab:blue")


def common_sentence_lengths(stats: Statistics, ax: Axes) -> None:
    sentence_lengths = stats.most_common_sentence_lengths(10)
    x_labels = [f"{length} words" for length, _count in sentence_lengths]
    counts = [count for _length, count in sentence_lengths]
    bar_colors = ["tab:green"]

    ax.set_ylabel("Occurances")
    ax.set_title("Most common sentence lengths")
    ax.tick_params(axis="x", labelrotation=45)
    ax.bar(x_labels, counts, color=bar_colors)


def character_analysis(stats: Statistics) -> Figure:
    fig, (ax1, ax2) = plt.subplots(1, 2)
    most_common_letters(stats, ax1)
    character_type_dist(stats, ax2)
    return fig


def most_common_letters(stats: Statistics, ax: Axes) -> None:
    most_common = stats.most_common_letters()
    x_labels = [letter for letter, _count in most_common]
    counts = [count for _letter, count in most_common]
    ax.set_ylabel("Occurances")
    ax.set_title("Most Common Letters")
    ax.bar(x_labels, counts, color="tab:purple")
