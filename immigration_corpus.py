"""
Immigration Discourse Dataset - Data Access Library

Simple, focused library for accessing ~126K immigration news articles from S3.
Includes in-memory caching for performance.

Requirements:
- AWS credentials in environment variables (use setup_aws.sh)
- Required packages: pandas, boto3, s3fs
"""

import pandas as pd
from typing import List, Optional, Dict
import os
import sys

# S3 Configuration
BUCKET = 'immigration-discourse-dataset'
PREFIX = 'data/'

# In-memory cache
# NOTE: No size limit currently - if memory becomes an issue, 
# consider adding max_cache_size parameter and LRU eviction
_CACHE = {}


def load_data(
    files: Optional[List[int]] = None,
    use_cache: bool = True,
    force_reload: bool = False
) -> pd.DataFrame:
    """
    Load immigration discourse data from S3
    
    Args:
        files: List of file indices (0-99). If None, loads all 100 files.
        use_cache: Use in-memory cache to avoid re-downloading (default: True)
        force_reload: Force reload even if cached (default: False)
    
    Returns:
        DataFrame with columns: source, url, title, header, text, authors, publish_date
    
    Example:
        >>> df = load_data(files=[0, 1, 2])
        >>> print(f"Loaded {len(df):,} articles")
    """
    if files is None:
        files = range(100) # type: ignore
    
    dfs = []
    for i in files: # type: ignore
        cache_key = f'articles_{i:03d}'
        
        # Check cache
        if use_cache and not force_reload and cache_key in _CACHE:
            dfs.append(_CACHE[cache_key])
            print(f"Cached articles_{i:03d}.jsonl ({len(_CACHE[cache_key]):,} articles)")
            continue
        
        # Load from S3
        try:
            df = pd.read_json(
                f's3://{BUCKET}/{PREFIX}articles_{i:03d}.jsonl',
                lines=True,
                storage_options={'anon': False}
            )
            
            # Cache it
            if use_cache:
                _CACHE[cache_key] = df
            
            dfs.append(df)
            print(f"Loaded articles_{i:03d}.jsonl ({len(df):,} articles)")
            
        except Exception as e:
            error_msg = str(e)
            
            # Check if it's a credentials error
            if 'credentials' in error_msg.lower() or 'access' in error_msg.lower():
                print(f"\nAWS Credentials Error!")
                print("\nPlease configure AWS credentials using one of these methods:")
                print("\n1. AWS CLI (recommended):")
                print("   pip install awscli")
                print("   aws configure")
                print("\n2. Environment variables:")
                print("   export AWS_ACCESS_KEY_ID='...'")
                print("   export AWS_SECRET_ACCESS_KEY='...'")
                print("\n3. Credentials file (~/.aws/credentials)")
                print("\nSee TEAM_GUIDE.md for details.")
                print(f"\nOriginal error: {e}\n")
                sys.exit(1)
            
            print(f"Failed to load articles_{i:03d}.jsonl: {e}")
    
    result = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
    
    if len(result) > 0:
        print(f"\nTotal: {len(result):,} articles")
    
    return result


def search_term(
    df: pd.DataFrame,
    term: str,
    case_sensitive: bool = False
) -> pd.DataFrame:
    """
    Search for articles containing a term
    
    Args:
        df: DataFrame to search
        term: Search term (supports regex)
        case_sensitive: Case-sensitive search (default: False)
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> results = search_term(df, 'illegal alien')
        >>> print(f"Found {len(results):,} articles")
    """
    mask = df['text'].fillna('').str.contains(
        term,
        case=case_sensitive,
        regex=True,
        na=False
    )
    return df[mask]


def get_term_counts(df: pd.DataFrame, terms: List[str]) -> Dict[str, Dict]:
    """
    Count occurrences of multiple terms
    
    Args:
        df: DataFrame to analyze
        terms: List of search terms
    
    Returns:
        Dictionary with counts and percentages for each term
    
    Example:
        >>> counts = get_term_counts(df, ['illegal alien', 'undocumented immigrant'])
        >>> for term, stats in counts.items():
        >>>     print(f"{term}: {stats['count']:,} ({stats['percentage']:.2f}%)")
    """
    results = {}
    for term in terms:
        mask = df['text'].fillna('').str.lower().str.contains(
            term.lower(),
            na=False
        )
        results[term] = {
            'count': mask.sum(),
            'percentage': (mask.sum() / len(df)) * 100 if len(df) > 0 else 0
        }
    return results


def load_sample(n: int = 1000, random_state: int = 42) -> pd.DataFrame:
    """
    Load random sample from first file (for testing)
    
    Args:
        n: Number of articles to sample (default: 1000)
        random_state: Random seed for reproducibility
    
    Returns:
        DataFrame with n random articles
    
    Example:
        >>> sample = load_sample(n=500)
    """
    df = load_data(files=[0])
    return df.sample(n=min(n, len(df)), random_state=random_state)


def filter_by_date(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Filter articles by publication date
    
    Args:
        df: DataFrame to filter
        start_date: Start date in ISO format (e.g., '2023-01-15')
        end_date: End date in ISO format (e.g., '2023-12-31')
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> filtered = filter_by_date(df, start_date='2023-01-01', end_date='2023-12-31')
    """
    # Work on a copy to avoid modifying original
    result = df.copy()
    
    # Convert publish_date to datetime (handles str, object, and datetime types)
    result['publish_date'] = pd.to_datetime(result['publish_date'], errors='coerce')
    
    # Filter by dates
    if start_date:
        start_dt = pd.to_datetime(start_date)
        result = result[result['publish_date'] >= start_dt]
    
    if end_date:
        end_dt = pd.to_datetime(end_date)
        result = result[result['publish_date'] <= end_dt]
    
    return result


def filter_by_source(df: pd.DataFrame, sources: List[str]) -> pd.DataFrame:
    """
    Filter articles by news source
    
    Args:
        df: DataFrame to filter
        sources: List of source names (e.g., ['cnn.com', 'foxnews.com'])
    
    Returns:
        Filtered DataFrame
    
    Example:
        >>> filtered = filter_by_source(df, ['breitbart.com', 'huffpost.com'])
    """
    return df[df['source'].isin(sources)]


def get_stats(df: pd.DataFrame) -> Dict:
    """
    Get dataset statistics
    
    Args:
        df: DataFrame to analyze
    
    Returns:
        Dictionary with statistics
    
    Example:
        >>> stats = get_stats(df)
        >>> print(f"Date range: {stats['date_range']}")
        >>> print(f"Top sources: {stats['top_sources']}")
    """
    # Convert dates to datetime (always, to handle str/object/datetime types)
    dates = pd.to_datetime(df['publish_date'], errors='coerce')
    
    stats = {
        'total_articles': len(df),
        'unique_sources': df['source'].nunique(),
        'date_range': (
            dates.min().strftime('%Y-%m-%d') if not dates.isna().all() else None,
            dates.max().strftime('%Y-%m-%d') if not dates.isna().all() else None
        ),
        'top_sources': df['source'].value_counts().head(10).to_dict(),
        'articles_with_dates': (~dates.isna()).sum(),
        'avg_text_length': df['text'].fillna('').str.len().mean()
    }
    
    return stats


def export_to_json(
    df: pd.DataFrame,
    filename: str,
    format: str = 'jsonl'
):
    """
    Export DataFrame to JSON file
    
    Args:
        df: DataFrame to export
        filename: Output filename
        format: 'jsonl' (default) or 'json'
    
    Example:
        >>> results = search_term(df, 'illegal alien')
        >>> export_to_json(results, 'illegal_alien_articles.jsonl')
    """
    if format == 'jsonl':
        df.to_json(filename, orient='records', lines=True)
        print(f"Exported {len(df):,} articles to {filename}")
    elif format == 'json':
        df.to_json(filename, orient='records', indent=2)
        print(f"Exported {len(df):,} articles to {filename}")
    else:
        raise ValueError("format must be 'jsonl' or 'json'")


def clear_cache():
    """
    Clear the in-memory cache
    
    Use this if you need to free up memory or force reload all files.
    
    Example:
        >>> clear_cache()
        >>> df = load_data(files=[0, 1, 2])  # Will reload from S3
    """
    global _CACHE
    cache_size = len(_CACHE)
    _CACHE.clear()
    print(f"Cleared cache ({cache_size} files)")


if __name__ == '__main__':
    # Quick test
    print("Testing immigration_corpus.py...\n")
    df = load_sample(n=100)
    print(f"\nLoaded {len(df)} sample articles")
    
    stats = get_stats(df)
    print(f"\nStats: {stats['total_articles']} articles from {stats['unique_sources']} sources")