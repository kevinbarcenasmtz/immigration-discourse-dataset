# Immigration Discourse Dataset
Repository for code related to querying the immigration dataset from a aws s3 bucket. News-scraper is a separate repo that did all the scraping for the dataset

~126,000 news articles about immigration from GDELT-indexed sources (2023-2025).

Data is hosted on AWS S3 for easy programmatic access with built-in caching.

## Quick Start

**Team member setup:**

- git clone https://github.com/kevinbarcenasmtz/immigration-discourse-dataset.git
- cd immigration-discourse-dataset
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- source setup_aws.sh  # Enter AWS credentials

**Start using the library:**
python examples/01_basic_loading.py

### 1. Setup

```bash
git clone https://github.com/kevinbarcenasmtz/immigration-discourse-dataset.git
cd immigration-discourse-dataset

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (one-time setup)
source setup_aws.sh  # Enter your AWS Access Key ID and Secret Key
```

### 2. Load and Analyze Data

```python
from immigration_corpus import load_data, search_term, get_term_counts

# Load first 3 files (automatically cached)
df = load_data(files=[0, 1, 2])

# Search for articles
results = search_term(df, 'illegal alien')
print(f"Found {len(results):,} articles")

# Compare term usage
counts = get_term_counts(df, ['illegal alien', 'undocumented immigrant'])
for term, stats in counts.items():
    print(f"{term}: {stats['count']:,} ({stats['percentage']:.2f}%)")
```

### 3. Run Example

```bash
python examples/01_basic_loading.py
```

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

## API Reference

### Core Functions

#### `load_data(files, use_cache=True, force_reload=False)`
Load articles from S3 with automatic caching.

```python
# Load specific files
df = load_data(files=[0, 1, 2])

# Load all files (warning: ~2.8GB in memory)
df = load_data()  # files=None loads all 100 files

# Force reload (ignore cache)
df = load_data(files=[0], force_reload=True)
```

#### `search_term(df, term, case_sensitive=False)`
Search for articles containing a term (supports regex).

```python
results = search_term(df, 'illegal alien')
results = search_term(df, 'illegal (alien|immigrant)', case_sensitive=False)
```

#### `get_term_counts(df, terms)`
Count occurrences of multiple terms.

```python
counts = get_term_counts(df, ['illegal alien', 'undocumented immigrant'])
# Returns: {'illegal alien': {'count': 3509, 'percentage': 2.78}, ...}
```

#### `load_sample(n=1000, random_state=42)`
Load random sample for testing.

```python
sample = load_sample(n=500)
```

### Utility Functions

#### `filter_by_date(df, start_date, end_date)`
Filter by publication date (ISO format).

```python
df_2023 = filter_by_date(df, start_date='2023-01-01', end_date='2023-12-31')
```

#### `filter_by_source(df, sources)`
Filter by news sources.

```python
fox_cnn = filter_by_source(df, ['foxnews.com', 'cnn.com'])
```

#### `get_stats(df)`
Get dataset statistics.

```python
stats = get_stats(df)
print(f"Total: {stats['total_articles']:,}")
print(f"Sources: {stats['unique_sources']}")
print(f"Date range: {stats['date_range']}")
print(f"Top sources: {stats['top_sources']}")
```

#### `export_to_json(df, filename, format='jsonl')`
Export filtered results.

```python
results = search_term(df, 'illegal alien')
export_to_json(results, 'output.jsonl', format='jsonl')  # or format='json'
```

#### `clear_cache()`
Clear in-memory cache to free memory.

```python
clear_cache()
```

## S3 Storage

- **Bucket**: `s3://immigration-discourse-dataset/data/`
- **Files**: `articles_000.jsonl` through `articles_099.jsonl`
- **Region**: `us-east-1`

## AWS Credentials

**Required**: AWS Access Key ID and Secret Access Key

Get credentials from your team lead, then run:
```bash
source setup_aws.sh
```

Credentials are stored in environment variables for the current terminal session only.

## Performance Tips

1. **Use caching** (enabled by default): Files are cached in memory after first load
2. **Load selectively**: Start with a few files, not all 100
3. **Use `load_sample()`** for development/testing
4. **Clear cache** if memory is an issue: `clear_cache()`

## Examples

See `examples/` directory:
- `01_basic_loading.py` - Core functionality walkthrough

## Related Repositories

The scraping code is in a separate repository: [news-scraper]
