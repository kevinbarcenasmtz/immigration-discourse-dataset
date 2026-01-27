"""
Immigration Corpus - Basic Loading Example

Demonstrates:
1. Loading data with caching
2. Searching for terms
3. Comparing term frequencies
4. Filtering by source
5. Getting dataset statistics
6. Exporting results
"""

from immigration_corpus import (
    load_data,
    search_term,
    get_term_counts,
    filter_by_source,
    get_stats,
    export_to_json,
)

print("=" * 60)
print("Immigration Discourse Dataset - Basic Example")
print("=" * 60)

# 1. Load first 3 files (cached automatically)
print("\n1. Loading data...")
df = load_data(files=[0, 1, 2])

# 2. Search for a specific term
print("\n2. Searching for 'illegal alien'...")
results = search_term(df, "illegal alien")
print(f"   Found {len(results):,} articles")

# 3. Compare multiple terms
print("\n3. Comparing terms...")
terms = ["illegal alien", "undocumented immigrant"]
counts = get_term_counts(df, terms)

for term, stats in counts.items():
    print(f"   {term}: {stats['count']:,} articles ({stats['percentage']:.2f}%)")

# 4. Filter by source
print("\n4. Filtering by source...")
fox_cnn = filter_by_source(df, ["foxnews.com", "cnn.com"])
print(f"   Fox News + CNN: {len(fox_cnn):,} articles")

# 5. Get dataset statistics
print("\n5. Dataset statistics...")
stats = get_stats(df)
print(f"   Total articles: {stats['total_articles']:,}")
print(f"   Unique sources: {stats['unique_sources']}")
print(f"   Date range: {stats['date_range'][0]} to {stats['date_range'][1]}")
print(f"   Avg text length: {stats['avg_text_length']:.0f} chars")

print("\n   Top 5 sources:")
for source, count in list(stats["top_sources"].items())[:5]:
    print(f"      {source}: {count:,}")

# 6. Export results (optional - commented out)
# print("\n6. Exporting results...")
# export_to_json(results, 'illegal_alien_articles.jsonl')

print("\n" + "=" * 60)
print("Example complete!")
print("=" * 60)

# Demonstrate cache reuse
print("\n TIP: Re-loading same files will use cache (much faster)")
print("Try running this script again to see caching in action!")
