# Reverse Uroman - Latin to Non-Latin Script Converter

This is a reverse implementation of the Uroman system that converts Latin script text to various non-Latin scripts, starting with Arabic support.

## Overview

The original Uroman system converts non-Latin scripts (Arabic, Devanagari, etc.) to Latin script. This reverse system does the opposite - it takes Latin text and converts it to non-Latin scripts.

## Features

- **Arabic Script Support**: Full Arabic character mapping with priority-based rule selection
- **Priority System**: More specific rules take precedence over general ones
- **Fallback Mapping**: Automatic fallback for unknown words/characters
- **Multiple Output Formats**: String, edges, or full lattice output
- **Caching**: Performance optimization with configurable cache size
- **Extensible**: Easy to add support for additional scripts

## Installation

1. Ensure you have Python 3.7+ installed
2. The system uses only standard library modules (no external dependencies)
3. Place the data files in the `reverse_data/` directory

## Usage

### Command Line Interface

```bash
# Basic usage
python reverse_uroman.py "hello world"

# Specify target script
python reverse_uroman.py "hello world" --script Arabic

# Different output formats
python reverse_uroman.py "hello world" --format edges
python reverse_uroman.py "hello world" --format lattice

# Help
python reverse_uroman.py --help
```

### Python API

```python
from reverse_uroman import ReverseUroman, ReverseRomFormat

# Create instance
reverse_uroman = ReverseUroman()

# Convert text
result = reverse_uroman.reverse_romanize_string("hello world", target_script="Arabic")
print(result)  # Output: هيللووأولد

# Get detailed edge information
edges = reverse_uroman.reverse_romanize_string(
    "hello world",
    target_script="Arabic",
    format=ReverseRomFormat.EDGES
)
for edge in edges:
    print(f"{edge.latin} → {edge.target}")
```

## Data Files

### reverse_arabic.txt

Contains Arabic-specific reverse romanization rules in the format:

```
latin::arabic::script::priority::context
```

Examples:

- `a::ا::Arabic::100` - Basic letter mapping
- `sh::ش::Arabic::200` - Digraph with higher priority
- `allah::الله::Arabic::500` - Full word with highest priority

### reverse_general.txt

Contains general patterns that apply across multiple scripts:

- Common English words
- Prefixes and suffixes
- Consonant clusters

## Priority System

Rules are ranked by priority (higher numbers = higher priority):

- **100**: Basic character mappings
- **150**: Consonant clusters
- **200**: Common digraphs and patterns
- **250**: Word endings
- **300**: Common words
- **400**: Phrases
- **500**: Names and special terms

## Architecture

### Core Classes

1. **ReverseUroman**: Main orchestrator class
2. **ReverseRomRule**: Individual romanization rules
3. **ReverseScript**: Script properties and rules
4. **ReverseLattice**: Graph representation of conversion paths
5. **ReverseEdge**: Individual conversion segments

### How It Works

1. **Rule Loading**: Loads reverse romanization rules from data files
2. **Lattice Building**: Creates edges for all possible Latin spans
3. **Priority Selection**: Chooses the best rule for each span based on priority
4. **Path Finding**: Finds optimal conversion path through the lattice
5. **Output Generation**: Produces result in requested format

## Adding New Scripts

To add support for a new script:

1. **Create data file**: `reverse_data/reverse_[scriptname].txt`
2. **Add script definition**: Update `load_script_definitions()` method
3. **Add fallback mapping**: Update `get_fallback_target()` method

Example for Devanagari:

```python
devanagari_script = ReverseScript(
    name="Devanagari",
    direction="left-to-right",
    default_vowels=["a"],
    vowel_insertion_rules={
        "consonant_final": "a",
        "consonant_medial": "a",
    }
)
```

## Testing

Run the test suite:

```bash
python test_reverse.py
```

The test suite covers:

- Basic conversions
- Sentence-level processing
- Different output formats
- Priority system
- Fallback mapping
- Script switching

## Examples

### Basic Conversions

- `hello` → `هيللو`
- `world` → `وأولد`
- `salam` → `سلام`
- `muhammad` → `محمد`

### Sentences

- `hello world` → `هيللووأولد`
- `muhammad ali` → `محمدعلي`
- `salam alaikum` → `سلامالايكوم`

### Priority Examples

- `sh` → `ش` (not `س` + `ه`)
- `th` → `ث` (not `ت` + `ه`)
- `kh` → `خ` (not `ك` + `ه`)

## Limitations

1. **Ambiguity**: Latin → non-Latin has higher ambiguity than the reverse
2. **Context**: Some conversions depend on surrounding context
3. **Script Selection**: User must specify target script
4. **Vowel Handling**: Abugida scripts need special vowel insertion logic

## Future Enhancements

1. **Context Awareness**: Better handling of surrounding text
2. **Language Detection**: Automatic script selection based on content
3. **Machine Learning**: Learn from user corrections
4. **More Scripts**: Support for additional writing systems
5. **Vowel Optimization**: Better abugida vowel handling

## Contributing

To contribute:

1. Add new rules to the data files
2. Improve the priority system
3. Add support for new scripts
4. Enhance the testing suite
5. Optimize performance

## License

Based on the original Uroman system by Ulf Hermjakob, USC/ISI.
