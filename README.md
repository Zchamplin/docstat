# DocStat — Documentation Scanner CLI

**Purpose**  
DocStat quickly scans Markdown/HTML docs and reports key metrics (word count, headings, image refs). This helps doc teams estimate translation scope, spot sparse pages, and prep for style/QA checks.

**Key Features**
- Recursive scan of directories
- Counts words, headings, and Markdown image references
- CSV or text output
- Simple filters (`--min-words`)

**Quick Start**
```bash
# In a virtual environment
pip install typer rich

# Scan current folder (text output)
python src/docstat/cli.py .

# Save a CSV report
python src/docstat/cli.py . --format csv --out report.csv

# Only include files with >= 50 words
python src/docstat/cli.py . -m 50 --format csv --out report.csv
