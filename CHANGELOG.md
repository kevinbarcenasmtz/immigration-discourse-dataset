# Changelog

All notable changes to the immigration-discourse-dataset will be documented here.

## [Unreleased]

### Planned (Subject to change)
- Media bias labels (custom classification or?)
- Sentiment analysis scores
- Topic modelring results
- Connotation vs denotation analysis
- Partisan word usage indicators

## [0.1.0] - 2025-01-27

### Added
- Initial release of immigration-discourse-dataset library
- Core data loading with s3 caching
- Search & filter utilities (`search_term`, `filter_by_date`, `filter_by_source`)
- Statistical analysis (`get_stats`, `get_term_counts`)
- Export functionality (`export_to_json`)
- Team onboarding documentation

### Dataset Schema
- `source`: News outlet domain
- `url`: Article URL
- `title`: Article headline
- `header`: Article subtitle
- `text`: Full article text
- `authors`: List of authors
- `publish_date`: ISO format timestamp
