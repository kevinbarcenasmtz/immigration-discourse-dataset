# Team Onboarding Guide

Quick guide for team members to start using the immigration corpus dataset.

## Setup (5 minutes)

### 1. Install the library

In your own research project:

```bash
# Create your project directory
cd ~/Projects
mkdir my-immigration-research
cd my-immigration-research

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the immigration-corpus library from GitHub
pip install git+https://github.com/kevinbarcenasmtz/immigration-discourse-dataset.git
```

### 2. Set AWS credentials

Get credentials, then configure AWS (one-time setup):

**Option A: AWS CLI (Recommended)**

```bash
# Install AWS CLI if needed
pip install awscli

# Configure (stores credentials securely in ~/.aws/)
aws configure

# When prompted, enter:
# AWS Access Key ID: <paste from Kevin>
# AWS Secret Access Key: <paste from Kevin>
# Default region: us-east-1
# Default output format: json
```

**Option B: Manual credentials file**

```bash
# Create AWS credentials file
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = YOUR_ACCESS_KEY_HERE
aws_secret_access_key = YOUR_SECRET_KEY_HERE
EOF

chmod 600 ~/.aws/credentials
```

**Option C: Environment variables (session-based)**

```bash
export AWS_ACCESS_KEY_ID="your-access-key-here"
export AWS_SECRET_ACCESS_KEY="your-secret-key-here"
export AWS_DEFAULT_REGION="us-east-1"
```

⚠️ **Note:** Options A & B persist across terminal sessions. Option C requires re-entering each session.

## Usage

### Jupyter Notebook Setup

If working in Jupyter notebooks, you have several options for AWS credentials:

**Option 1: AWS CLI (recommended - one-time setup)**
```bash
# In terminal, before starting Jupyter:
aws configure  # Enter credentials once
jupyter notebook  # All notebooks work automatically
```

**Option 2: Set credentials at top of notebook**
```python
import os

# Set before importing immigration_corpus
os.environ['AWS_ACCESS_KEY_ID'] = 'your-key-here'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your-secret-here'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

from immigration_corpus import load_data
df = load_data(files=[0, 1, 2])
```
⚠️ **Warning:** Don't commit notebooks with credentials! Add to .gitignore.

**Option 3: Load from external file (more secure)**
```python
# Create aws_config.py (add to .gitignore):
# AWS_ACCESS_KEY_ID = 'your-key'
# AWS_SECRET_ACCESS_KEY = 'your-secret'

import os
from aws_config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY

from immigration_corpus import load_data
df = load_data(files=[0, 1, 2])
```

**Option 4: Prompt for credentials (most secure)**
```python
import os
from getpass import getpass

os.environ['AWS_ACCESS_KEY_ID'] = getpass('AWS Access Key: ')
os.environ['AWS_SECRET_ACCESS_KEY'] = getpass('AWS Secret: ')

from immigration_corpus import load_data
df = load_data(files=[0, 1, 2])
```

### Basic Example

```python
from immigration_corpus import load_data, search_term, get_term_counts

# Load first 3 files (~19K articles)
df = load_data(files=[0, 1, 2])

# Search for a term
results = search_term(df, 'illegal alien')
print(f"Found {len(results):,} articles")

# Compare terms
counts = get_term_counts(df, ['illegal alien', 'undocumented immigrant'])
for term, stats in counts.items():
    print(f"{term}: {stats['count']:,} ({stats['percentage']:.2f}%)")
```

### Working with Your Own Analysis

```python
import pandas as pd
from immigration_corpus import load_data, filter_by_date, filter_by_source

# Load data
df = load_data(files=range(10))  # First 10 files

# Filter to your needs
df_2023 = filter_by_date(df, start_date='2023-01-01', end_date='2023-12-31')
conservative_sources = filter_by_source(df, ['breitbart.com', 'foxnews.com'])

# Your analysis

# Save results
df_2023.to_csv('my_analysis.csv', index=False)
```

## Available Functions

```python
from immigration_corpus import (
    load_data,           # Load articles with caching
    search_term,         # Search for specific terms
    get_term_counts,     # Count term occurrences
    filter_by_date,      # Filter by publication date
    filter_by_source,    # Filter by news source
    get_stats,           # Get dataset statistics
    export_to_json,      # Export filtered results
    load_sample,         # Quick testing with sample data
    clear_cache,         # Free up memory
)
```

See the [README](https://github.com/kevinbarcenasmtz/immigration-discourse-dataset) for full documentation.

## Dataset Schema

Each article has:
- `source`: News outlet (e.g., "cnn.com")
- `url`: Article URL
- `title`: Headline
- `text`: Full article text
- `authors`: List of authors
- `publish_date`: ISO format timestamp

## Updating

When owner adds new annotations:

```bash
pip install --upgrade git+https://github.com/kevinbarcenasmtz/immigration-discourse-dataset.git
```

## Tips

1. **Start small**: Use `load_sample(n=1000)` or `load_data(files=[0])` for testing
2. **Cache is automatic**: Files are cached in memory - reloading is instant
3. **Memory management**: Use `clear_cache()` if you run out of memory
4. **Export for sharing**: Use `export_to_json()` to share filtered datasets with team

## Getting Help

- **Documentation**: https://github.com/kevinbarcenasmtz/immigration-discourse-dataset
- **Issues**: Contact owner or open GitHub issue
- **AWS Access**: Contact owner for credentials