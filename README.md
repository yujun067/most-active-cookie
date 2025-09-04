# Most Active Cookie Finder

A production-ready command-line tool to find the most active cookie for a specific date from cookie log files.


## 🎯 Description

Given a cookie log file in CSV format, this tool processes the log and returns the most active cookie (the one seen most times) during a given day. If multiple cookies have the same highest count, all of them are returned on separate lines.

**Key Features:**
- **High Performance**: Processes 50K+ entries in <0.1 seconds
- **Robust Error Handling**: Graceful handling of malformed data
- **Memory Efficient**: Streaming CSV processing with early termination
- **Production Ready**: Comprehensive test suite with 86% coverage

## 🚀 Quick Start

### Installation

See the [Development Setup](#setup-development-environment) section below for detailed installation instructions.

### Basic Usage

```bash
python src/main.py -f cookie_log.csv -d 2018-12-09
```

## 📋 Usage Guide

### Command Line Interface

```bash
python src/main.py [OPTIONS]
```

**Required Arguments:**
- `-f, --filename PATH`: Path to the cookie log CSV file
- `-d, --date DATE`: Target date in YYYY-MM-DD format

**Optional Arguments:**
- `-v, --verbose`: Enable detailed debug output
- `-h, --help`: Show help message and exit

### Examples

**Basic usage:**
```bash
python src/main.py -f sample_cookie_log.csv -d 2018-12-09
```
Output:
```
AtY0laUfhglK3lC7
```

**Multiple cookies with same count (tie):**
```bash
python src/main.py -f sample_cookie_log.csv -d 2018-12-08
```
Output:
```
4sMM2LxV07bPJzwf
SAZuXPGUrfbcn5UA
fbcn5UAVanZf6UtG
```

**With verbose output:**
```bash
python src/main.py -f sample_cookie_log.csv -d 2018-12-09 --verbose
```

**No data for date:**
```bash
python src/main.py -f sample_cookie_log.csv -d 2020-01-01
```
Output: (empty - no cookies found for that date)

## 📄 Input Format

The input CSV file should have the following format:

```csv
cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
```

### Requirements

- CSV file with header row: `cookie,timestamp`
- Timestamps in ISO format (e.g., `2018-12-09T14:19:00+00:00`)
- Data sorted by timestamp (most recent first)
- UTF-8 encoding
- Any file size (memory-efficient processing)

### Sample Data

We provide sample test data in the `tests/fixtures/` directory:
- `sample_log.csv` - Basic example from requirements
- `tie_scenario.csv` - Multiple cookies with same count
- `malformed_missing_fields.csv` - Example with data quality issues

## ⚙️ Exit Codes

| Code | Meaning | Example |
|------|---------|---------|
| `0` | Success | Cookie found and displayed |
| `1` | Runtime error | File permission denied, CSV parsing failed, unexpected error |
| `2` | Usage error + User interrupt | Invalid arguments, file not found, Ctrl+C interrupt |

## 🔧 Development & Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup Development Environment

```bash
# Clone and setup
git clone <repository-url>
cd most-active-cookie

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src

# Run specific test file
python -m pytest tests/test_integration.py -v
```

### Code Quality

```bash
# Format code
python -m black src/ tests/

# Lint code  
python -m flake8 src/ tests/

# Type checking  
python -m mypy src/
```

### Testing Different Scenarios

```bash
# Test with sample data
python src/main.py -f tests/fixtures/sample_log.csv -d 2018-12-09

# Test error handling
python src/main.py -f nonexistent.csv -d 2018-12-09

# Test with verbose output
python src/main.py -f tests/fixtures/sample_log.csv -d 2018-12-09 --verbose
```

### Performance Testing

```bash
# Run comprehensive performance tests
python tests/test_performance.py

# This will test with datasets from 1K to 1M entries and measure:
# - Processing time and throughput
# - Memory usage
# - Scalability characteristics
```

## Project Structure

```
most-active-cookie/
├── src/
│   ├── main.py              # Main application entry point
│   ├── arg_parser.py        # Command-line argument parser
│   ├── cookie_log_processor.py  # Core cookie processing logic
│   ├── logging_config.py    # Centralized logging configuration
│   └── __init__.py          # Package initialization
├── tests/                  # Test suite
│   ├── test_cli.py         # CLI argument parsing tests
│   ├── test_cookie_log_processor.py # Core logic unit tests
│   ├── test_integration.py # End-to-end integration tests
│   ├── test_performance.py # Performance and scalability tests
│   └── fixtures/           # Test data files
├── sample_cookie_log.csv    # Example data file for demos
├── requirements.txt         # Development dependencies
├── pyproject.toml          # Tool configuration (Black, MyPy, pytest)
├── setup.cfg               # Flake8 configuration
└── README.md               # Project documentation
```

