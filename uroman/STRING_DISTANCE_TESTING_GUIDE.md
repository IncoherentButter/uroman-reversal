# String Distance Testing for Reverse Uroman

This guide explains how to use string distance metrics to evaluate the quality of reverse romanization in the uroman system.

## Overview

String distance metrics provide a sophisticated way to measure the quality of reverse romanization by comparing expected outputs with actual outputs. This is particularly useful for:

- **Quality Assessment**: Measuring how well reverse romanization preserves the original meaning
- **Round-trip Testing**: Testing the complete cycle of Original → Romanized → Reverse Romanized
- **Error Analysis**: Identifying common types of errors in reverse romanization
- **Performance Benchmarking**: Comparing different reverse romanization approaches

## Available Testing Tools

### 1. Python-based String Distance (`reverse_string_distance_python.py`)

A pure Python implementation that doesn't require Perl dependencies.

**Features:**

- Custom cost rules for character substitutions
- Normalized distance calculation (0-1 scale)
- Support for different scripts (Arabic, Swahili, etc.)
- Round-trip and direct testing modes

**Usage:**

```python
from reverse_string_distance_python import ReverseStringDistanceTester

tester = ReverseStringDistanceTester()

# Test direct reverse romanization
test_cases = [
    {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
    {'latin': 'jambo', 'expected': 'jambo', 'script': 'Swahili'},
]

results = tester.test_direct_reverse_romanization(test_cases)
print(tester.generate_report(results))
```

### 2. Perl-based String Distance (`reverse_string_distance_test.py`)

Uses the original Perl string-distance.pl script with sophisticated cost rules.

**Features:**

- Language-aware cost rules
- Context-sensitive character substitutions
- Support for complex linguistic patterns
- Integration with existing uroman evaluation framework

**Usage:**

```python
from reverse_string_distance_test import ReverseStringDistanceTester

tester = ReverseStringDistanceTester()

# Test round-trip romanization
original_texts = ["سلام", "محمد"]
language_codes = ["ara", "ara"]
target_scripts = ["Arabic", "Arabic"]

results = tester.test_round_trip_romanization(original_texts, language_codes, target_scripts)
```

### 3. Comprehensive Test Suite (`test_reverse_with_string_distance.py`)

A complete testing framework with predefined test datasets.

**Usage:**

```bash
# Quick demo
python test_reverse_with_string_distance.py --demo

# Full comprehensive tests
python test_reverse_with_string_distance.py --full
```

## Test Types

### 1. Direct Reverse Romanization Testing

Tests the accuracy of reverse romanization against known expected outputs.

**Example:**

```python
test_cases = [
    {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
    {'latin': 'muhammad', 'expected': 'محمد', 'script': 'Arabic'},
]

results = tester.test_direct_reverse_romanization(test_cases)
```

**Metrics:**

- String distance (raw edit distance)
- Normalized distance (0-1 scale)
- Success rate (based on threshold)
- Character-level accuracy

### 2. Round-trip Testing

Tests the complete cycle: Original → Romanized → Reverse Romanized.

**Example:**

```python
original_texts = ["السلام عليكم", "أهلاً وسهلاً"]
language_codes = ["ara", "ara"]
target_scripts = ["Arabic", "Arabic"]

results = tester.test_round_trip_romanization(original_texts, language_codes, target_scripts)
```

**Benefits:**

- Tests the complete pipeline
- Identifies cumulative errors
- Measures information preservation

### 3. Script-specific Testing

Focused testing for specific scripts with detailed error analysis.

**Example:**

```python
arabic_cases = [
    {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
    {'latin': 'kitab', 'expected': 'كتاب', 'script': 'Arabic'},
]

results = tester.test_script_specific_accuracy('Arabic', arabic_cases)
```

## String Distance Metrics

### 1. Raw String Distance

The minimum number of character-level operations (insertions, deletions, substitutions) needed to transform one string into another.

**Cost Rules:**

- Vowels: 0.1 (very similar)
- Consonants: 1.0 (more significant differences)
- Special cases: Custom costs (e.g., 'f' → 'ph': 0.01)

### 2. Normalized Distance

Raw distance divided by the maximum string length, providing a 0-1 scale where:

- 0.0 = Identical strings
- 1.0 = Completely different strings

### 3. Success Thresholds

- **Direct testing**: < 0.3 (stricter)
- **Round-trip testing**: < 0.5 (more lenient)

## Interpreting Results

### Success Rate

Percentage of tests that meet the success threshold.

### Average Distance

Mean string distance across all test cases.

### Error Analysis

Classification of error types:

- Character substitution
- Character insertion
- Character deletion
- Word boundary errors
- Diacritic errors

## Example Output

```
REVERSE UROMAN STRING DISTANCE TEST REPORT
============================================================

Test Type: direct_reverse

SUMMARY STATISTICS
------------------------------
Total Samples: 10
Successful Samples: 8
Success Rate: 80.00%
Average Distance: 1.200
Average Normalized Distance: 0.240

SAMPLE DETAILS
------------------------------
Sample 0:
  Latin Input: salam
  Expected: سلام
  Actual: سالام
  Distance: 1.000
  Normalized Distance: 0.200
  Success: True
```

## Best Practices

### 1. Test Dataset Creation

- Include diverse vocabulary
- Cover different linguistic patterns
- Include edge cases and common errors
- Balance between simple and complex examples

### 2. Threshold Selection

- Adjust thresholds based on script complexity
- Consider the intended use case
- Balance between precision and recall

### 3. Error Analysis

- Focus on systematic errors
- Identify patterns in failures
- Use results to improve reverse romanization rules

### 4. Performance Monitoring

- Track metrics over time
- Compare different approaches
- Monitor improvements after rule updates

## Integration with Existing Evaluation

The string distance testing can be integrated with the existing uroman evaluation framework:

```python
from evaluation.metrics.character_error_rate import CharacterErrorRate
from evaluation.metrics.word_error_rate import WordErrorRate

# Use alongside existing metrics
cer_metric = CharacterErrorRate()
wer_metric = WordErrorRate()

# Combine with string distance testing
string_distance_results = tester.test_direct_reverse_romanization(test_cases)
cer_results = cer_metric.calculate(reference_texts, hypothesis_texts)
wer_results = wer_metric.calculate(reference_texts, hypothesis_texts)
```

## Troubleshooting

### Common Issues

1. **Missing data files**: Ensure all required data files are in the correct locations
2. **Perl dependencies**: For Perl-based testing, ensure Perl and required modules are installed
3. **Encoding issues**: Ensure all text is properly UTF-8 encoded
4. **Memory usage**: For large test datasets, consider batch processing

### Performance Optimization

1. **Caching**: Use caching for repeated calculations
2. **Batch processing**: Process multiple test cases together
3. **Parallel processing**: Use multiprocessing for large datasets
4. **Memory management**: Clear intermediate results when not needed

## Future Enhancements

1. **Language-specific cost rules**: Implement script-specific substitution costs
2. **Context-aware testing**: Consider linguistic context in distance calculations
3. **Machine learning integration**: Use ML models for error prediction
4. **Visualization tools**: Create charts and graphs for result analysis
5. **Automated reporting**: Generate HTML/PDF reports with visualizations

## Conclusion

String distance metrics provide a powerful tool for evaluating reverse romanization quality. By combining different testing approaches and metrics, you can gain comprehensive insights into the performance of your reverse romanization system and identify areas for improvement.
