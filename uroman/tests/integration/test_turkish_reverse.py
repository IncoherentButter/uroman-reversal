#!/usr/bin/env python3
"""
Test script for Turkish reverse romanization
Demonstrates how the reverse romanization rules would work
"""

def test_turkish_reverse_romanization():
    """Test various Turkish reverse romanization patterns"""
    
    test_cases = [
        # Basic Turkish characters
        ("c", "ç"),
        ("g", "ğ"),
        ("i", "ı"),
        ("o", "ö"),
        ("s", "ş"),
        ("u", "ü"),
        
        # Common Turkish words
        ("merhaba", "merhaba"),
        ("tesekkur", "teşekkür"),
        ("guzel", "güzel"),
        ("cok", "çok"),
        ("iyi", "iyi"),
        ("nasil", "nasıl"),
        ("nerede", "nerede"),
        ("ne", "ne"),
        ("kim", "kim"),
        ("zaman", "zaman"),
        ("ev", "ev"),
        ("kitap", "kitap"),
        ("su", "su"),
        ("yemek", "yemek"),
        ("okul", "okul"),
        ("araba", "araba"),
        ("sehir", "şehir"),
        ("ulke", "ülke"),
        ("insan", "insan"),
        ("cocuk", "çocuk"),
        
        # Turkish phrases
        ("Merhaba nasilsin?", "Merhaba nasılsın?"),
        ("Tesekkur ederim.", "Teşekkür ederim."),
        ("Cok guzel bir gun.", "Çok güzel bir gün."),
        ("Nerede yasiyorsun?", "Nerede yaşıyorsun?"),
        ("Bu kitap cok guzel.", "Bu kitap çok güzel."),
    ]
    
    print("🇹🇷 Turkish Reverse Romanization Test")
    print("=" * 60)
    print("Testing Turkish reverse romanization patterns...")
    print()
    
    # Load the reverse romanization system
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from reverse_uroman import ReverseUroman
        reverse_uroman = ReverseUroman()
        print("✅ Reverse Uroman system loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load reverse uroman system: {e}")
        return
    
    print()
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (input_text, expected) in enumerate(test_cases, 1):
        try:
            # Apply reverse romanization
            result = reverse_uroman.reverse_romanize_string(input_text, target_script="Turkish")
            
            # Check if result matches expected
            success = result == expected
            if success:
                success_count += 1
            
            status = "✅" if success else "❌"
            print(f"{i:2d}. {status} '{input_text}' -> '{result}'")
            if not success:
                print(f"    Expected: '{expected}'")
            
        except Exception as e:
            print(f"{i:2d}. ❌ '{input_text}' -> ERROR: {e}")
    
    print()
    print("=" * 60)
    print(f"📊 Results: {success_count}/{total_count} tests passed ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total_count - success_count} tests failed")


def test_turkish_character_mapping():
    """Test individual Turkish character mappings"""
    
    print("\n🔤 Turkish Character Mapping Test")
    print("=" * 40)
    
    # Load the reverse romanization system
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from reverse_uroman import ReverseUroman
        reverse_uroman = ReverseUroman()
    except Exception as e:
        print(f"❌ Failed to load reverse uroman system: {e}")
        return
    
    # Test individual characters
    characters = [
        ("c", "ç"),
        ("g", "ğ"), 
        ("i", "ı"),
        ("o", "ö"),
        ("s", "ş"),
        ("u", "ü"),
    ]
    
    for latin, expected_turkish in characters:
        try:
            result = reverse_uroman.reverse_romanize_string(latin, target_script="Turkish")
            success = result == expected_turkish
            status = "✅" if success else "❌"
            print(f"{status} '{latin}' -> '{result}' (expected: '{expected_turkish}')")
        except Exception as e:
            print(f"❌ '{latin}' -> ERROR: {e}")


def test_turkish_word_boundaries():
    """Test Turkish word boundary handling"""
    
    print("\n📝 Turkish Word Boundary Test")
    print("=" * 40)
    
    # Load the reverse romanization system
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    try:
        from reverse_uroman import ReverseUroman
        reverse_uroman = ReverseUroman()
    except Exception as e:
        print(f"❌ Failed to load reverse uroman system: {e}")
        return
    
    # Test phrases with spaces
    phrases = [
        "merhaba dunya",      # hello world
        "cok guzel",          # very beautiful
        "tesekkur ederim",    # thank you
        "nasil gidiyor",      # how is it going
    ]
    
    for phrase in phrases:
        try:
            result = reverse_uroman.reverse_romanize_string(phrase, target_script="Turkish")
            print(f"'{phrase}' -> '{result}'")
        except Exception as e:
            print(f"'{phrase}' -> ERROR: {e}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Turkish reverse romanization")
    parser.add_argument("--characters", action="store_true", help="Test character mappings")
    parser.add_argument("--words", action="store_true", help="Test word mappings")
    parser.add_argument("--boundaries", action="store_true", help="Test word boundaries")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.all or (not args.characters and not args.words and not args.boundaries):
        # Run all tests by default
        test_turkish_reverse_romanization()
        test_turkish_character_mapping()
        test_turkish_word_boundaries()
    else:
        if args.words:
            test_turkish_reverse_romanization()
        if args.characters:
            test_turkish_character_mapping()
        if args.boundaries:
            test_turkish_word_boundaries()


if __name__ == "__main__":
    main()
