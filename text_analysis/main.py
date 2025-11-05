import sys
from tracemalloc import Statistic

import text_analysis.plots as plots
from text_analysis import analysis
from text_analysis.book import Book
from text_analysis.stats import Statistics
from text_analysis.tui import pick_book, prompt_selection


def main():
    print("Pick a book to analyze")
    book_path = pick_book()
    with Book(book_path) as book:
        stats = Statistics()
        for chunk in book:
            stats.analyze_chunk(chunk)
    while True:
        analysis_kind = prompt_selection(
            ["basic", "word", "sentence", "character", "report", "exit"]
        )[1]
        if analysis_kind == "basic":
            print(analysis.basic(stats))
        elif analysis_kind == "word":
            print(analysis.word_analysis(stats))
        elif analysis_kind == "sentence":
            print(analysis.sentence_analysis(stats))
        elif analysis_kind == "character":
            ...
        elif analysis_kind == "report":
            export_report(stats)
        elif analysis_kind == "exit":
            sys.exit(0)

        next_step = prompt_selection(["new_analysis", "plot", "exit"])[1]
        if next_step == "new_book":
            main()
        elif next_step == "new_analysis":
            continue
        elif next_step == "plot":
            plots.show_plot(analysis_kind, stats)
        elif next_step == "exit":
            sys.exit(0)


def export_report(stats: Statistics) -> None:
    report = analysis.report(stats)
    with open("report.txt", "w") as f:
        _ = f.write(report)

if __name__ == "__main__":
    main()
