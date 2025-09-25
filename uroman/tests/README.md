# Uroman Test Suite

This directory contains all test files for the uroman and reverse-uroman systems, organized by test type.

## Directory Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for full workflows
├── debug/          # Debug and diagnostic tests
├── run_full_test_suite.py  # Comprehensive test suite runner
└── README.md       # This file
```

## Test Categories

### Unit Tests (`tests/unit/`)

- `test_forward_spaces.py` - Tests space handling in forward romanization
- `test_reverse_spaces.py` - Tests space handling in reverse romanization

### Integration Tests (`tests/integration/`)

- `test_reverse_with_string_distance.py` - Full integration test with string distance metrics
- `test_turkish_cli.py` - CLI integration tests for Turkish
- `test_turkish_reverse.py` - Turkish reverse romanization tests
- `test_reverse.py` - General reverse romanization tests

### Debug Tests (`tests/debug/`)

- `test_swahili_debug.py` - Debug tests for Swahili with detailed output

### Test Suite Runner (`tests/`)

- `run_full_test_suite.py` - Comprehensive test runner that executes all test categories and provides detailed reporting

## Running Tests

### Run all tests:

```bash
# Comprehensive test suite (recommended)
python tests/run_full_test_suite.py

# Or use pytest
python -m pytest tests/
```

### Run specific test categories:

```bash
# Unit tests only
python -m pytest tests/unit/

# Integration tests only
python -m pytest tests/integration/

# Debug tests only
python -m pytest tests/debug/
```

### Run individual tests:

```bash
# Forward romanization space test
python tests/unit/test_forward_spaces.py

# Reverse romanization space test
python tests/unit/test_reverse_spaces.py

# Full string distance integration test
python tests/integration/test_reverse_with_string_distance.py --demo
```

## Test Data

Test data files are located in:

- `mini-test/` - Small test datasets
- `reverse_data/` - Reverse romanization data files
- `test_turkish_samples.txt` - Turkish test samples

## Documentation

- `TESTING_GUIDE.md` - General testing guidelines
- `STRING_DISTANCE_TESTING_GUIDE.md` - String distance testing guide
- `README_REVERSE.md` - Reverse romanization documentation
