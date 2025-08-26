#!/usr/bin/env python3
"""
CLI Test Script for Turkish Reverse Romanization
Run this to see how the transformations work
"""

def apply_turkish_reverse_rules(text):
    """Apply Turkish reverse romanization rules (simplified version)"""
    
    # Load the reverse romanization rules
    rules = {
        # High priority letter mappings
        'Ch': 'Ç', 'ch': 'ç',
        'Sh': 'Ş', 'sh': 'ş',
        
        # Vowel diacritics
        'Oe': 'Ö', 'oe': 'ö',
        'Ue': 'Ü', 'ue': 'ü',
        
        # Double vowel to ğ patterns
        'aa': 'ağ', 'ee': 'eğ', 'ii': 'iğ',
        'oo': 'oğ', 'uu': 'uğ',
        
        # Place name specific rules
        'Istanbul': 'İstanbul',
        'Izmir': 'İzmir',
        'Diyarbakir': 'Diyarbakır',
        'Eskisehir': 'Eskişehir',
        'Elazig': 'Elazığ',
        
        # Common word patterns
        'Tuerkiye': 'Türkiye',
        'shehir': 'şehir',
        'uelke': 'ülke',
        'teshekkuer': 'teşekkür',
        'yashayan': 'yaşayan',
        'arkadashimla': 'arkadaşımla',
        'bulushtum': 'buluştum',
        'cok': 'çok',
        'guzel': 'güzel',
        'yapmak': 'yapmak',
        'gittim': 'gittim',
        'dogdugum': 'doğduğum',
        'kebap': 'kebap',
        'golu': 'gölü',
        'etrafinda': 'etrafında',
        'dolastim': 'dolaştım',
        'endustrisi': 'endüstrisi',
        
        # Numbers and basic words
        'uc': 'üç', 'dort': 'dört', 'bes': 'beş',
        'alti': 'altı', 'yedi': 'yedi', 'sekiz': 'sekiz',
        'dokuz': 'dokuz', 'on': 'on',
        
        # Colors
        'Kirmizi': 'Kırmızı', 'kirmizi': 'kırmızı',
        'yeshil': 'yeşil', 'sari': 'sarı',
        'Kahverengi': 'Kahverengi', 'kahverengi': 'kahverengi',
        'turuncu': 'turuncu', 'pembe': 'pembe',
        'lacivert': 'lacivert',
        
        # Family and food
        'kardesh': 'kardeş', 'cocuk': 'çocuk',
        'chay': 'çay', 'balik': 'balık',
        'sebze': 'sebze', 'meyve': 'meyve',
        'sut': 'süt', 'peynir': 'peynir',
        'yumurta': 'yumurta', 'pilav': 'pilav',
        
        # Time and weather
        'Bugun': 'Bugün', 'bugun': 'bugün',
        'dun': 'dün', 'yarin': 'yarın',
        'shimdi': 'şimdi', 'ogle': 'öğle',
        'aksham': 'akşam', 'guneshli': 'güneşli',
        'yagmurlu': 'yağmurlu', 'karli': 'karlı',
        'ruzgarli': 'rüzgarlı', 'sicak': 'sıcak',
        'soguk': 'soğuk',
        
        # Verbs
        'Gitmek': 'Gitmek', 'gitmek': 'gitmek',
        'gelmek': 'gelmek', 'yapmak': 'yapmak',
        'gormek': 'görmek', 'duymak': 'duymak',
        'soylemek': 'söylemek', 'almak': 'almak',
        'vermek': 'vermek', 'sevmek': 'sevmek',
        'istemek': 'istemek', 'bilmek': 'bilmek',
        'anlamak': 'anlamak', 'calishmak': 'çalışmak',
        'okumak': 'okumak', 'yazmak': 'yazmak',
        
        # Additional patterns
        'yashiyorsun': 'yaşıyorsun',
        'yashindasin': 'yaşındasın',
        'geleceksin': 'geleceksin',
        'bulushtum': 'buluştum',
        'mutlu': 'mutlu', 'oldum': 'oldum',
        'hava': 'hava', 'durumu': 'durumu',
        'disari': 'dışarı', 'cikmak': 'çıkmak',
        'tatil': 'tatil', 'eglendim': 'eğlendim',
        'anilar': 'anılar', 'biriktirdim': 'biriktirdim',
        'giderken': 'giderken', 'yol': 'yol',
        'uzerinde': 'üzerinde', 'manzaralar': 'manzaralar',
        'gordum': 'gördüm', 'cocukluk': 'çocukluk',
        'gecirdim': 'geçirdim'
    }
    
    # Apply rules in order of priority (longer patterns first)
    result = text
    for latin, turkish in sorted(rules.items(), key=lambda x: len(x[0]), reverse=True):
        result = result.replace(latin, turkish)
    
    return result

def test_single_transformations():
    """Test individual transformations"""
    print("=== Individual Transformations ===")
    
    test_cases = [
        ("Ch", "Ç"),
        ("ch", "ç"),
        ("Sh", "Ş"),
        ("sh", "ş"),
        ("Oe", "Ö"),
        ("oe", "ö"),
        ("Ue", "Ü"),
        ("ue", "ü"),
        ("aa", "ağ"),
        ("ee", "eğ"),
        ("ii", "iğ"),
        ("oo", "oğ"),
        ("uu", "uğ"),
    ]
    
    for latin, expected in test_cases:
        result = apply_turkish_reverse_rules(latin)
        status = "✓" if result == expected else "✗"
        print(f"{status} {latin:5} → {result:5} (expected: {expected})")

def test_place_names():
    """Test Turkish place name transformations"""
    print("\n=== Place Names ===")
    
    place_names = [
        "Istanbul",
        "Izmir", 
        "Diyarbakir",
        "Eskisehir",
        "Elazig",
        "Ankara",
        "Antalya",
        "Konya",
        "Van golu",
        "Batman"
    ]
    
    for place in place_names:
        result = apply_turkish_reverse_rules(place)
        print(f"  {place:15} → {result}")

def test_common_words():
    """Test common Turkish word transformations"""
    print("\n=== Common Words ===")
    
    words = [
        "Merhaba",
        "teshekkuer",
        "guzel",
        "cok",
        "evet",
        "hayir",
        "tamam",
        "peki"
    ]
    
    for word in words:
        result = apply_turkish_reverse_rules(word)
        print(f"  {word:15} → {result}")

def test_complex_sentences():
    """Test complex sentence transformations"""
    print("\n=== Complex Sentences ===")
    
    sentences = [
        "Istanbul'da yashayan arkadashimla bulushtum.",
        "Ankara'nin hava durumu bugun cok guzel.",
        "Antalya'da tatil yapmak istiyorum.",
        "Eskisehir'den Konya'ya gittim."
    ]
    
    for sentence in sentences:
        result = apply_turkish_reverse_rules(sentence)
        print(f"  Original: {sentence}")
        print(f"  Result:   {result}")
        print()

def interactive_mode():
    """Interactive mode for testing custom text"""
    print("\n=== Interactive Mode ===")
    print("Enter Turkish text to test (or 'quit' to exit):")
    
    while True:
        try:
            text = input("\n> ").strip()
            if text.lower() in ['quit', 'exit', 'q']:
                break
            if text:
                result = apply_turkish_reverse_rules(text)
                print(f"Result: {result}")
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("Goodbye!")

def main():
    """Main function"""
    print("Turkish Reverse Romanization Test Script")
    print("=" * 50)
    
    test_single_transformations()
    test_place_names()
    test_common_words()
    test_complex_sentences()
    
    # Ask if user wants interactive mode
    try:
        response = input("\nWould you like to test custom text? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_mode()
    except (KeyboardInterrupt, EOFError):
        pass
    
    print("\nTest completed!")

if __name__ == "__main__":
    main()

