# Turkish Reverse Romanization

This document explains the Turkish reverse romanization system implemented in `reverse_turkish.txt`.

## Overview

The Turkish reverse romanization system converts Latin script text back to proper Turkish text with correct diacritics and special characters.

## Turkish-Specific Letters

Turkish has several letters that don't exist in English:

| Latin | Turkish | Description                            |
| ----- | ------- | -------------------------------------- |
| Ç/ç   | Ç/ç     | C with cedilla (like "ch" in "church") |
| Ğ/ğ   | Ğ/ğ     | G with breve (vowel lengthener)        |
| I/ı   | I/ı     | Dotless i (close back unrounded vowel) |
| İ/i   | İ/i     | Dotted i (close front unrounded vowel) |
| Ö/ö   | Ö/ö     | O with diaeresis (front rounded vowel) |
| Ş/ş   | Ş/ş     | S with cedilla (like "sh" in "ship")   |
| Ü/ü   | Ü/ü     | U with diaeresis (front rounded vowel) |

## Reverse Romanization Rules

### 1. Letter Mappings (Priority 500)

- **Ch → Ç** (capital)
- **ch → ç** (lowercase)
- **Sh → Ş** (capital)
- **sh → ş** (lowercase)

### 2. Vowel Diacritics (Priority 400)

- **Oe → Ö** (capital)
- **oe → ö** (lowercase)
- **Ue → Ü** (capital)
- **ue → ü** (lowercase)

### 3. Double Vowel to ğ Patterns (Priority 400)

- **aa → ağ** (long a → a + ğ)
- **ee → eğ** (long e → e + ğ)
- **ii → iğ** (long i → i + ğ)
- **oo → oğ** (long o → o + ğ)
- **uu → uğ** (long u → u + ğ)

### 4. Context-Dependent Vowel Rules

- **I → İ**: When in Turkish context (capital dotted i)
- **I → ı**: When in Turkish context (capital dotless i)
- **i → i**: No change needed (lowercase dotted i)
- **i → ı**: When in Turkish context (lowercase dotless i)

## Priority System

The system uses a priority-based approach:

- **Priority 600**: Turkish place names and very common words
- **Priority 500**: Turkish-specific letter mappings and phrases
- **Priority 400**: Vowel patterns and medium-priority words
- **Priority 300**: Basic letter mappings

Higher priority rules override lower priority ones.

## Examples

### Basic Transformations

```
Ch → Ç          (ch → ç)
Sh → Ş          (sh → ş)
Oe → Ö          (oe → ö)
Ue → Ü          (ue → ü)
aa → ağ         (long vowel → vowel + ğ)
```

### Place Names

```
Istanbul → İstanbul
Izmir → İzmir
Diyarbakir → Diyarbakır
Eskisehir → Eskişehir
Elazig → Elazığ
```

### Common Words

```
evet → evet
teşekkür → teşekkür
merhaba → merhaba
günaydın → günaydın
```

## Usage

The reverse romanization table is used by the uroman system when:

1. **Language code is Turkish**: `::lcode tur`
2. **Turkish context is detected**: Based on word patterns and place names
3. **Manual selection**: User specifies Turkish reverse romanization

## File Format

The `reverse_turkish.txt` file follows the standard format:

```
latin::target::script::priority::context
```

Example:

```
Ch::Ç::Turkish::500
ch::ç::Turkish::500
Istanbul::İstanbul::Turkish::600
```

## Testing

Use the `test_turkish_reverse.py` script to test various transformation patterns:

```bash
cd uroman
python test_turkish_reverse.py
```

## Notes

- **Context sensitivity**: Some rules (like I → İ vs I → ı) require Turkish context
- **Ğ placement**: Ğ always follows vowels in Turkish, never at word beginning
- **Vowel harmony**: Turkish has vowel harmony rules that affect pronunciation
- **Loan words**: Some words may retain their original spelling

## Future Enhancements

Potential improvements could include:

- Vowel harmony rule implementation
- Context-aware I/İ/ı/i selection
- Loan word handling
- Dialect-specific variations
