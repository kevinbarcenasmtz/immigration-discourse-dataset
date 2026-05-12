# Immigration Discourse Dataset

Repository for code related to querying the immigration dataset from an AWS S3 bucket. The news-scraper is a separate repo that did all the scraping for the dataset. Data is hosted on AWS S3 for easy programmatic access with built-in caching.

## One-Time Setup

```powershell
git clone https://github.com/kevinbarcenasmtz/immigration-discourse-dataset.git
cd immigration-discourse-dataset

# Create and activate virtual environment (Windows/PowerShell)
C:\Users\Kevin\anaconda3\python.exe -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies and the library
pip install -r requirements.txt
pip install -e .
```

> **Linux/Mac:** `python3 -m venv venv && source venv/bin/activate`

## Each Session

```powershell
# 1. Activate venv
.\venv\Scripts\Activate.ps1

# 2. Set AWS credentials (session-only — cleared when terminal closes)
$env:AWS_ACCESS_KEY_ID     = "your-key-id"
$env:AWS_SECRET_ACCESS_KEY = "your-secret-key"
$env:AWS_DEFAULT_REGION    = "us-east-1"

# 3. Launch Jupyter (always launch from the activated venv)
jupyter notebook
```

The default `python3` kernel in Jupyter will use your venv's Python. No kernel switching needed as long as Jupyter is launched from the activated venv.

## Quick Start

```python
from immigration_corpus import load_data, search_term, get_term_counts

# Load first 3 files (~19K articles, cached automatically)
df = load_data(files=[0, 1, 2])

# Search for articles
results = search_term(df, 'illegal alien')
print(f"Found {len(results):,} articles")

# Compare term usage
counts = get_term_counts(df, ['illegal alien', 'undocumented immigrant'])
for term, stats in counts.items():
    print(f"{term}: {stats['count']:,} ({stats['percentage']:.2f}%)")
```

See `examples/jupyter_template.ipynb` for a full walkthrough notebook.

## Dataset Schema

Each article contains:

| Field          | Type | Description                                         |
| -------------- | ---- | --------------------------------------------------- |
| `source`       | str  | News outlet domain (e.g., "cnn.com")                |
| `url`          | str  | Article URL                                         |
| `title`        | str  | Article headline                                    |
| `header`       | str  | Article subtitle/description                        |
| `text`         | str  | Full article text                                   |
| `authors`      | list | List of author names                                |
| `publish_date` | str  | ISO format date (e.g., "2023-05-04T09:12:04+00:00") |

## S3 Storage

- **Bucket**: `s3://immigration-discourse-dataset/data/`
- **Files**: `articles_000.jsonl` through `articles_099.jsonl` (~2.8GB total)
- **Region**: `us-east-1`

## API Reference

### `load_data(files=None, use_cache=True, force_reload=False)`
Load articles from S3. `files` is a list of indices 0–99. Default loads all 100 files (warning: ~2.8GB in memory).

```python
df = load_data(files=[0, 1, 2])          # ~19K articles
df = load_data(files=range(10))          # first 10 files
df = load_data(files=[0], force_reload=True)  # skip cache
```

### `load_sample(n=1000, random_state=42)`
Load a random sample from the first file — use this for development/testing.

### `search_term(df, term, case_sensitive=False)`
Filter to articles containing a term (supports regex).

### `get_term_counts(df, terms)`
Count occurrences of multiple terms. Returns `{term: {'count': int, 'percentage': float}}`.

### `filter_by_date(df, start_date, end_date)`
Filter by `publish_date`. Dates in ISO format (`'2023-01-01'`).

### `filter_by_source(df, sources)`
Filter by news source domain list (e.g., `['foxnews.com', 'cnn.com']`).

### `get_stats(df)`
Returns total articles, unique sources, date range, top 10 sources, avg text length.

### `export_to_json(df, filename, format='jsonl')`
Export a filtered DataFrame to `.jsonl` or `.json`.

### `clear_cache()`
Clear the in-memory file cache to free memory.

## AWS Credentials

Credentials are session-only (cleared when terminal closes). Get your Access Key ID and Secret Access Key from the team lead.

For a persistent setup use `aws configure` (requires `pip install awscli`) — credentials are then stored in `~/.aws/credentials` and no environment variables are needed each session.

## Related Repositories

The scraping code is in a separate repository: [news-scraper]
