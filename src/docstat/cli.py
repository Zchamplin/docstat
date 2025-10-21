import sys
import csv
from pathlib import Path
import typer

def scan(
    path: Path = typer.Argument(
        Path("."), help="Folder to scan (default: current directory)"
    ),
    min_words: int = typer.Option(
        0, "--min-words", "-m", help="Only include files with at least this many words"
    ),
    out: Path | None = typer.Option(
        None, "--out", "-o", help="Write results to a CSV file (e.g., report.csv)"
    ),
    format: str = typer.Option(
        "text", "--format", "-f", help="Output format: text or csv"
    ),
):
    """
    Scan a folder for .md and .html files and report word/heading/image counts.
    """
    format = format.lower().strip()
    if format not in {"text", "csv"}:
        typer.secho("Error: --format must be 'text' or 'csv'.", fg=typer.colors.RED)
        raise typer.Exit(code=2)

    typer.echo(f"Scanning {path} ...")

    if not path.exists():
        typer.secho(f"Error: {path} does not exist.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    rows: list[tuple[str, str, int, int, int]] = []
    for file in path.rglob("*"):
        if file.is_file() and file.suffix.lower() in {".md", ".html"}:
            try:
                text = file.read_text(encoding="utf-8", errors="ignore")
            except Exception as e:
                typer.secho(f"Could not read {file}: {e}", fg=typer.colors.YELLOW)
                continue

            words = len(text.split())
            if words < min_words:
                continue

            # rough counts (good enough for v1)
            headings = text.count("#")          # Markdown headings
            images = text.count("![](")         # Markdown image refs

            rows.append((str(file), file.suffix.lower(), words, headings, images))

            if format == "text" and out is None:
                # streaming text output to console
                typer.echo(f"{file} — {words} words, {headings} headings, {images} images")

    if format == "csv":
        # write to file if --out is provided, otherwise to stdout
        headers = ("path", "ext", "words", "headings", "images")
        if out:
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            typer.secho(f"Wrote CSV: {out}", fg=typer.colors.GREEN)
        else:
            writer = csv.writer(sys.stdout)
            writer.writerow(headers)
            writer.writerows(rows)
    else:
        # text mode with --out: still write CSV if user asked for a file
        if out:
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(("path", "ext", "words", "headings", "images"))
                writer.writerows(rows)
            typer.secho(f"Wrote CSV (from text mode): {out}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    typer.run(scan)
