import curses
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
            export_report(stats)
        elif analysis_kind == "Exit the program":
            sys.exit(0)

        next_step = prompt_selection(
            win,
            "",
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
            filename = plots.show_plot(analysis_kind, stats)
            show(win, "Plot info", f"Plot exported to: {filename}")
        elif next_step == "Exit the program":
            sys.exit(0)


def export_report(stats: Statistics) -> None:
    report = stats.report()
    report_output = json.dumps(report, indent=2)
    timestamp = datetime.now().strftime("%m-%d_%H:%M")
    with open(f"reports/report_{timestamp}.json", "w") as f:
        _ = f.write(report_output)


def main():
    curses.wrapper(book_analysis)


if __name__ == "__main__":
    main()
