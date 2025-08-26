#!/usr/bin/env python3
"""
Test script for Turkish reverse romanization
Demonstrates how the reverse romanization rules would work
"""

def test_turkish_reverse_romanization():
    """Test various Turkish reverse romanization patterns"""
    
    test_cases = [
        # Basic letter mappings
        ("Ch", "Ç"),
        ("ch", "ç"),
        ("Sh", "Ş"),
        ("sh", "ş"),
        
        # Vowel diacritics
        ("Oe", "Ö"),
        ("oe", "ö"),
        ("Ue", "Ü"),
        ("ue", "ü"),
        
        # Double vowel to ğ patterns
        ("aa", "ağ"),
        ("ee", "eğ"),
        ("ii", "iğ"),
        ("oo", "oğ"),
        ("uu", "uğ"),
        
        # Place names
        ("Istanbul", "İstanbul"),
        ("Izmir", "İzmir"),
        ("Diyarbakir", "Diyarbakır"),
        ("Eskisehir", "Eskişehir"),
        ("Elazig", "Elazığ"),
        
        # Common words
        ("evet", "evet"),
        ("teşekkür", "teşekkür"),
        ("merhaba", "merhaba"),
        ("günaydın", "günaydın"),
        
        # Numbers
        ("bir", "bir"),
        ("iki", "iki"),
        ("üç", "üç"),
        ("dört", "dört"),
        ("beş", "beş"),
        
        # Colors
        ("kırmızı", "kırmızı"),
        ("mavi", "mavi"),
        ("yeşil", "yeşil"),
        ("sarı", "sarı"),
        
        # Family words
        ("anne", "anne"),
        ("baba", "baba"),
        ("kardeş", "kardeş"),
        ("abla", "abla"),
        
        # Food words
        ("ekmek", "ekmek"),
        ("çay", "çay"),
        ("kahve", "kahve"),
        ("et", "et"),
        
        # Time words
        ("bugün", "bugün"),
        ("dün", "dün"),
        ("yarın", "yarın"),
        ("şimdi", "şimdi"),
        
        # Weather words
        ("güneşli", "güneşli"),
        ("yağmurlu", "yağmurlu"),
        ("karlı", "karlı"),
        ("sıcak", "sıcak"),
        ("soğuk", "soğuk"),
        
        # Verbs
        ("gitmek", "gitmek"),
        ("gelmek", "gelmek"),
        ("yapmak", "yapmak"),
        ("görmek", "görmek"),
    ]
    
    print("Turkish Reverse Romanization Test Cases")
    print("=" * 50)
    
    for latin, expected in test_cases:
        # In a real implementation, this would use the reverse romanization table
        # For now, we'll just show what the expected output should be
        print(f"{latin:15} → {expected}")
    
    print("\n" + "=" * 50)
    print("Note: This is a demonstration of expected outputs.")
    print("Real implementation would use the reverse_turkish.txt table.")
    print("Priority system ensures more specific rules override general ones.")

def show_priority_examples():
    """Show how the priority system works"""
    
    print("\nPriority System Examples:")
    print("=" * 40)
    
    examples = [
        ("Ch", "Ç", "500", "Turkish-specific letter mapping (highest)"),
        ("ch", "ç", "500", "Turkish-specific letter mapping (highest)"),
        ("Istanbul", "İstanbul", "600", "Turkish place name (very high)"),
        ("Oe", "Ö", "400", "Turkish vowel diacritic (high)"),
        ("aa", "ağ", "400", "Turkish double vowel pattern (high)"),
        ("a", "a", "300", "Basic Turkish letter (medium)"),
    ]
    
    for latin, target, priority, description in examples:
        print(f"{latin:12} → {target:12} (Priority: {priority}) - {description}")

if __name__ == "__main__":
    test_turkish_reverse_romanization()
    show_priority_examples()
