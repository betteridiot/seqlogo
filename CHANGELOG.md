# Changelog

All notable changes to seqlogo will be documented in this file.

## [5.29.10] - 2026-01-27

### Changed
- **BREAKING**: Default format changed from 'svg' to 'png'
  - Improves compatibility with Jupyter, RMarkdown/reticulate, and Windows
  - SVG still available but requires pdf2svg installation
  
### Added
- Support for Python 3.4 through 3.13+
- Dynamic handling of pkg_resources (deprecated in Python 3.11+)
- Graceful fallback for version detection across Python versions
- Comprehensive error messages for SVG format when pdf2svg is missing
- Better documentation for Jupyter and RMarkdown usage

### Fixed
- Compatibility issues with modern Python versions (3.11+)
- Issues with setuptools deprecations
- Problems using seqlogo in RMarkdown with reticulate
- Installation failures on Windows

### Improved
- Error messages now provide actionable solutions
- Inline display in Jupyter Notebooks more reliable
- Documentation includes RMarkdown examples

