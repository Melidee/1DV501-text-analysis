import curses
import os
import sys
import json
from datetime import datetime

import text_analysis.plots as plots
from text_analysis.book import Book
from text_analysis.stats import Statistics
from text_analysis.tui import (
    basic,
    pick_book,
    prompt_selection,
    show,
    word_analysis,
    sentence_analysis,
    character_analysis,
)


def book_analysis(win: curses.window):
    win_setup(win)
    book_path = pick_book(win)
    with Book(book_path) as book:
        stats = Statistics()
        for chunk in book:
            stats.analyze_chunk(chunk)
    while True:
        analysis_kind = prompt_selection(
            win,
            "What kind of analysis would you like?",
            [
                "Basic Analysis",
                "Word Analysis",
                "Sentence Analysis",
                "Character Analysis",
                "Export JSON Report",
                "Exit the program",
            ],
        )
        if analysis_kind == "Basic Analysis":
            show(win, "Basic Analysis", basic(stats))
        elif analysis_kind == "Word Analysis":
            show(win, "Word Analysis", word_analysis(stats))
        elif analysis_kind == "Sentence Analysis":
            show(win, "Sentence Analysis", sentence_analysis(stats))
        elif analysis_kind == "Character Analysis":
            show(win, "Character Analysis", character_analysis(stats))
        elif analysis_kind == "Export JSON Report":
            filename = export_report(stats)
            show(win, "Report info", f"Plot exported to: {filename}")
        elif analysis_kind == "Exit the program":
            sys.exit(0)

        next_step = prompt_selection(
            win,
            f"What to do next with {book.title()}",
            [
                "Pick a new book",
                f"Perform a new analysis on {book_path}",
                f"Export plot for {analysis_kind}",
                "Exit the program",
            ],
        )
        if next_step == "Pick a new book":
            book_analysis(win)
        elif next_step == f"Perform a new analysis on {book_path}":
            continue
        elif next_step == f"Export plot for {analysis_kind}":
            filename = plots.show_plot(analysis_kind, stats, book)
            show(win, "Plot info", f"Plot exported to: {filename}")
        elif next_step == "Exit the program":
            sys.exit(0)


def win_setup(win: curses.window):
    win.clear()
    win.refresh()


def export_report(stats: Statistics) -> str:
    report = stats.report()
    report_output = json.dumps(report, indent=2)
    # get current timestamp
    timestamp = datetime.now().strftime("%m-%d_%H:%M")
    file_name = f"reports/report_{timestamp}.json"
    # create report dir if it doesn't exist
    os.makedirs(os.path.dirname("./reports/"), exist_ok=True)
    with open(file_name, "w") as f:
        _ = f.write(report_output)
    return file_name


def main():
    curses.wrapper(book_analysis)


if __name__ == "__main__":
    main()
