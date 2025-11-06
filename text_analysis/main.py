import curses
import sys

import text_analysis.plots as plots
from text_analysis import analysis
from text_analysis.book import Book
from text_analysis.stats import Statistics
from text_analysis.tui import pick_book, prompt_selection, show


def start(win: curses.window):
    win.clear()
    win.refresh()
    book_path = pick_book(win)
    with Book(book_path) as book:
        stats = Statistics()
        for chunk in book:
            stats.analyze_chunk(chunk)
    while True:
        analysis_kind = prompt_selection(
            win,
            "Pick one",
            ["basic", "word", "sentence", "character", "report", "exit"],
        )
        if analysis_kind == "basic":
            show(win, "Basic Analysis", analysis.basic(stats))
        elif analysis_kind == "word":
            show(win, "Word Analysis", analysis.word_analysis(stats))
        elif analysis_kind == "sentence":
            show(win, "Sentence Analysis", analysis.sentence_analysis(stats))
        elif analysis_kind == "character":
            show(win, "Character Analysis", analysis.character_analysis(stats))
        elif analysis_kind == "report":
            export_report(stats)
        elif analysis_kind == "exit":
            sys.exit(0)

        next_step = prompt_selection(win, "Pick one", ["new_book", "new_analysis", "plot", "exit"])
        if next_step == "new_book":
            start(win)
        elif next_step == "new_analysis":
            continue
        elif next_step == "plot":
            plots.show_plot(analysis_kind, stats)
        elif next_step == "exit":
            sys.exit(0)


def export_report(stats: Statistics) -> None:
    report = analysis.report(stats)
    with open("report.json", "w") as f:
        _ = f.write(report)


def main():
    curses.wrapper(start)


if __name__ == "__main__":
    main()
