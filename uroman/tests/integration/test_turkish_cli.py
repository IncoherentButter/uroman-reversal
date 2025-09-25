#!/usr/bin/env python3
"""
CLI Test Script for Turkish Reverse Romanization
Run this to see how the transformations work
"""

def apply_turkish_reverse_rules(text):
    """Apply Turkish reverse romanization rules (simplified version)"""
    
    # Load the reverse romanization rules
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from reverse_uroman import ReverseUroman
    
    reverse_uroman = ReverseUroman()
    return reverse_uroman.reverse_romanize_string(text, target_script="Turkish")


def test_turkish_samples():
    """Test with sample Turkish words"""
    
    # Sample Turkish words in Latin script
    test_words = [
        "merhaba",      # hello
        "teşekkür",     # thank you  
        "güzel",        # beautiful
        "çok",          # very/much
        "iyi",          # good
        "nasıl",        # how
        "nerede",       # where
        "ne",           # what
        "kim",          # who
        "zaman",        # time
        "ev",           # house
        "kitap",        # book
        "su",           # water
        "yemek",        # food
        "okul",         # school
        "araba",        # car
        "şehir",        # city
        "ülke",         # country
        "insan",        # person
        "çocuk",        # child
    ]
    
    print("🇹🇷 Turkish Reverse Romanization Test")
    print("=" * 50)
    print("Testing Turkish words with reverse romanization...")
    print()
    
    for word in test_words:
        try:
            result = apply_turkish_reverse_rules(word)
            print(f"'{word}' -> '{result}'")
        except Exception as e:
            print(f"'{word}' -> ERROR: {e}")


def test_turkish_phrases():
    """Test with Turkish phrases"""
    
    phrases = [
        "Merhaba nasılsın?",           # Hello, how are you?
        "Teşekkür ederim.",            # Thank you.
        "Çok güzel bir gün.",          # It's a very beautiful day.
        "Nerede yaşıyorsun?",          # Where do you live?
        "Bu kitap çok güzel.",         # This book is very beautiful.
    ]
    
    print("\n🇹🇷 Turkish Phrase Test")
    print("=" * 50)
    print("Testing Turkish phrases with reverse romanization...")
    print()
    
    for phrase in phrases:
        try:
            result = apply_turkish_reverse_rules(phrase)
            print(f"'{phrase}' -> '{result}'")
        except Exception as e:
            print(f"'{phrase}' -> ERROR: {e}")


def interactive_test():
    """Interactive testing mode"""
    print("\n🇹🇷 Interactive Turkish Test")
    print("=" * 50)
    print("Enter Turkish words or phrases to test (type 'quit' to exit):")
    print()
    
    while True:
        try:
            user_input = input("Turkish text: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if user_input:
                result = apply_turkish_reverse_rules(user_input)
                print(f"Result: '{result}'")
                print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Turkish reverse romanization")
    parser.add_argument("--words", action="store_true", help="Test Turkish words")
    parser.add_argument("--phrases", action="store_true", help="Test Turkish phrases")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.all or (not args.words and not args.phrases and not args.interactive):
        # Run all tests by default
        test_turkish_samples()
        test_turkish_phrases()
        interactive_test()
    else:
        if args.words:
            test_turkish_samples()
        if args.phrases:
            test_turkish_phrases()
        if args.interactive:
            interactive_test()


if __name__ == "__main__":
    main()
