# Directory Organization Summary

This document summarizes the organization of test files and directories in the uroman project.

## ✅ Completed Organization

### Test Directory Structure

```
uroman/tests/
├── unit/                                    # Unit tests for individual components
│   ├── test_forward_spaces.py              # Tests space handling in forward romanization
│   └── test_reverse_spaces.py              # Tests space handling in reverse romanization
├── integration/                            # Integration tests for full workflows
│   ├── test_reverse_with_string_distance.py # Full integration test with string distance metrics
│   ├── test_reverse.py                     # General reverse romanization tests
│   ├── test_turkish_cli.py                 # CLI integration tests for Turkish
│   └── test_turkish_reverse.py             # Turkish reverse romanization tests
├── debug/                                  # Debug and diagnostic tests
│   └── test_swahili_debug.py               # Debug tests for Swahili with detailed output
├── dashboard/                              # Interactive dashboards and visualization
│   └── metrics_dashboard.py                # Comprehensive metrics dashboard
├── run_full_test_suite.py                  # Comprehensive test suite runner
└── README.md                               # Test documentation and usage guide
```

### Key Improvements Made

1. **Organized Test Structure**: Created a clear hierarchy of test types
2. **Moved All Test Files**: Relocated scattered test files into organized directories
3. **Updated Import Paths**: Fixed import statements to work with new directory structure
4. **Created Documentation**: Added comprehensive README for test suite
5. **Cleaned Up**: Removed duplicate files from root directory

### Test Categories

#### Unit Tests (`tests/unit/`)

- **Purpose**: Test individual components in isolation
- **Files**:
  - `test_forward_spaces.py` - Tests space preservation in forward romanization
  - `test_reverse_spaces.py` - Tests space preservation in reverse romanization

#### Integration Tests (`tests/integration/`)

- **Purpose**: Test complete workflows and system interactions
- **Files**:
  - `test_reverse_with_string_distance.py` - Full string distance evaluation system
  - `test_reverse.py` - General reverse romanization functionality
  - `test_turkish_cli.py` - Turkish CLI integration tests
  - `test_turkish_reverse.py` - Turkish-specific reverse romanization tests

#### Debug Tests (`tests/debug/`)

- **Purpose**: Diagnostic tests with detailed output for troubleshooting
- **Files**:
  - `test_swahili_debug.py` - Swahili debugging with detailed string distance analysis

### Test Suite Runner (`tests/`)

- **Purpose**: Comprehensive test suite that runs all tests and provides detailed reporting
- **Files**:
  - `run_full_test_suite.py` - Complete test runner with 6 test categories and summary reporting

### Dashboard (`tests/dashboard/`)

- **Purpose**: Interactive dashboards and visualization tools for metrics analysis
- **Files**:
  - `simple_dashboard.py` - Simple metrics dashboard with all 5 metrics (WER, MER, WIL, WIP, CER)
  - `metrics_dashboard.py` - Advanced metrics dashboard (requires matplotlib)

## 🚀 How to Run Tests

### Run All Tests

```bash
# From project root - Run comprehensive test suite
python uroman/tests/run_full_test_suite.py

# Or run individual test files
python uroman/tests/unit/test_forward_spaces.py
python uroman/tests/integration/test_reverse_with_string_distance.py --demo
python uroman/tests/integration/test_simple_metrics.py
python uroman/tests/debug/test_swahili_debug.py

# Run the simple metrics dashboard
python uroman/tests/dashboard/simple_dashboard.py

# Or use pytest for individual categories
python -m pytest uroman/tests/unit/
python -m pytest uroman/tests/integration/
python -m pytest uroman/tests/debug/
```

### Run by Category

```bash
# Unit tests only
python -m pytest uroman/tests/unit/

# Integration tests only
python -m pytest uroman/tests/integration/

# Debug tests only
python -m pytest uroman/tests/debug/
```

## 📁 Other Important Directories

### Core System Files

- `uroman/` - Main uroman system files
- `uroman/data/` - Data files for romanization rules
- `uroman/reverse_data/` - Reverse romanization data files
- `uroman/evaluation/` - Evaluation framework and metrics

### Documentation

- `uroman/README_REVERSE.md` - Reverse romanization documentation
- `uroman/TESTING_GUIDE.md` - General testing guidelines
- `uroman/STRING_DISTANCE_TESTING_GUIDE.md` - String distance testing guide
- `uroman/tests/README.md` - Test suite documentation

### Test Data

- `uroman/mini-test/` - Small test datasets
- `uroman/test_turkish_samples.txt` - Turkish test samples

## ✨ Benefits of This Organization

1. **Clear Separation**: Easy to find tests by type and purpose
2. **Maintainable**: Well-documented and organized structure
3. **Scalable**: Easy to add new tests in appropriate categories
4. **Professional**: Follows standard testing directory conventions
5. **Accessible**: Clear documentation for running and understanding tests
6. **Comprehensive Testing**: Single command runs all tests with detailed reporting

## 🔧 Future Maintenance

- Add new unit tests to `tests/unit/`
- Add new integration tests to `tests/integration/`
- Add new debug tests to `tests/debug/`
- Update `tests/README.md` when adding new test categories
- Keep test documentation synchronized with code changes
