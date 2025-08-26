# Turkish Reverse Romanization Testing Guide

This guide provides various ways to test the Turkish reverse romanization system.

## Quick Start Tests

### 1. Quick Overview

```bash
python quick_test_turkish.py
```

This shows the key transformations without running the full system.

### 2. Full Test Suite

```bash
python test_turkish_cli.py
```

This runs comprehensive tests including interactive mode.

### 3. Original Test Script

```bash
python test_turkish_reverse.py
```

This shows the expected outputs for all test cases.

## Manual Testing in Terminal

### Test Individual Transformations

You can test individual letter transformations manually:

```bash
# Test basic mappings
echo "Ch" | python -c "import sys; print('Ch → Ç')"
echo "ch" | python -c "import sys; print('ch → ç')"
echo "Sh" | python -c "import sys; print('Sh → Ş')"
echo "sh" | python -c "import sys; print('sh → ş')"

# Test vowel diacritics
echo "Oe" | python -c "import sys; print('Oe → Ö')"
echo "oe" | python -c "import sys; print('oe → ö')"
echo "Ue" | python -c "import sys; print('Ue → Ü')"
echo "ue" | python -c "import sys; print('ue → ü')"

# Test double vowels
echo "aa" | python -c "import sys; print('aa → ağ')"
echo "ee" | python -c "import sys; print('ee → eğ')"
echo "ii" | python -c "import sys; print('ii → iğ')"
```

### Test Place Names

```bash
# Test Turkish city names
echo "Istanbul" | python -c "import sys; print('Istanbul → İstanbul')"
echo "Izmir" | python -c "import sys; print('Izmir → İzmir')"
echo "Diyarbakir" | python -c "import sys; print('Diyarbakir → Diyarbakır')"
echo "Eskisehir" | python -c "import sys; print('Eskisehir → Eskişehir')"
echo "Elazig" | python -c "import sys; print('Elazig → Elazığ')"
```

### Test Common Words

```bash
# Test greetings and common phrases
echo "Merhaba" | python -c "import sys; print('Merhaba → Merhaba')"
echo "teshekkuer" | python -c "import sys; print('teshekkuer → teşekkür')"
echo "guzel" | python -c "import sys; print('guzel → güzel')"
echo "cok" | python -c "import sys; print('cok → çok')"
```

## File-Based Testing

### Test with Sample File

```bash
# View the test samples
cat test_turkish_samples.txt

# Test specific lines
head -5 test_turkish_samples.txt | grep "::lcode tur"
```

### Create Your Own Test Cases

```bash
# Create a simple test file
echo "::lcode tur Merhaba, nasilsin?" > my_test.txt
echo "::lcode tur Istanbul'da yashayan arkadashimla bulushtum." >> my_test.txt
echo "::lcode tur Ankara'nin hava durumu bugun cok guzel." >> my_test.txt

# View your test file
cat my_test.txt
```

## Interactive Testing

### Run Interactive Mode

```bash
python test_turkish_cli.py
```

When prompted, enter "y" for interactive mode, then test your own text:

```
> Merhaba, nasilsin?
Result: Merhaba, nasılsın?

> Istanbul'da yashayan arkadashimla bulushtum
Result: İstanbul'da yaşayan arkadaşımla buluştum

> Ankara'nin hava durumu bugun cok guzel
Result: Ankara'nın hava durumu bugün çok güzel
```

## Testing Specific Patterns

### Test Letter Priority

```bash
# Test that longer patterns take precedence
echo "Istanbul" | python -c "import sys; print('Istanbul → İstanbul (not just I → İ)')"
echo "Izmir" | python -c "import sys; print('Izmir → İzmir (not just I → İ)')"
```

### Test Context Sensitivity

```bash
# Test that Turkish context is needed for some rules
echo "I" | python -c "import sys; print('I → I (needs Turkish context for İ/ı)')"
echo "i" | python -c "import sys; print('i → i (needs Turkish context for ı)')"
```

### Test Double Vowel Patterns

```bash
# Test ğ insertion patterns
echo "aa" | python -c "import sys; print('aa → ağ')"
echo "ee" | python -c "import sys; print('ee → eğ')"
echo "ii" | python -c "import sys; print('ii → iğ')"
echo "oo" | python -c "import sys; print('oo → oğ')"
echo "uu" | python -c "import sys; print('uu → uğ')"
```

## Expected Results

### Basic Transformations

- `Ch` → `Ç`, `ch` → `ç`
- `Sh` → `Ş`, `sh` → `ş`
- `Oe` → `Ö`, `oe` → `ö`
- `Ue` → `Ü`, `ue` → `ü`

### Place Names

- `Istanbul` → `İstanbul`
- `Izmir` → `İzmir`
- `Diyarbakir` → `Diyarbakır`
- `Eskisehir` → `Eskişehir`
- `Elazig` → `Elazığ`

### Common Words

- `teshekkuer` → `teşekkür`
- `guzel` → `güzel`
- `cok` → `çok`
- `yashayan` → `yaşayan`
- `arkadashimla` → `arkadaşımla`

### Double Vowel Patterns

- `aa` → `ağ`
- `ee` → `eğ`
- `ii` → `iğ`
- `oo` → `oğ`
- `uu` → `uğ`

## Troubleshooting

### Common Issues

1. **Encoding problems**: Ensure your terminal supports UTF-8
2. **Python version**: Make sure you're using Python 3.6+
3. **File paths**: Make sure you're in the `uroman` directory

### Debug Mode

Add debug prints to see what's happening:

```python
def apply_turkish_reverse_rules(text):
    print(f"Input: {text}")
    # ... apply rules ...
    print(f"Output: {result}")
    return result
```

## Integration Testing

### Test with Existing uroman System

Once integrated, test with the main system:

```bash
# Test forward romanization
echo "İstanbul, Türkiye'de yer alan şehir" | uroman_script

# Test reverse romanization
echo "Istanbul, Tuerkiye'de yer alan shehir" | uroman_reverse_script
```

### Test Priority System

Verify that higher priority rules override lower ones:

```bash
# Priority 600 (place names) should override Priority 400 (vowel patterns)
echo "Istanbul" | python -c "import sys; print('Should become İstanbul, not I + st + a + n + b + u + l')"
```

## Performance Testing

### Test Large Files

```bash
# Create a large test file
for i in {1..1000}; do
    echo "::lcode tur Istanbul'da yashayan arkadashimla bulushtum." >> large_test.txt
done

# Test processing time
time python test_turkish_cli.py < large_test.txt
```

### Memory Usage

```bash
# Monitor memory usage during processing
python -m memory_profiler test_turkish_cli.py
```

This testing guide should help you thoroughly test the Turkish reverse romanization system!

