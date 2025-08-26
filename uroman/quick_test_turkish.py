#!/usr/bin/env python3
"""
Quick Test Script for Turkish Reverse Romanization
Simple examples you can run quickly
"""

def quick_test():
    """Quick test of key transformations"""
    
    print("Quick Turkish Reverse Romanization Test")
    print("=" * 40)
    
    # Test basic letter mappings
    print("1. Basic Letter Mappings:")
    print("   Ch → Ç")
    print("   ch → ç")
    print("   Sh → Ş")
    print("   sh → ş")
    print()
    
    # Test vowel diacritics
    print("2. Vowel Diacritics:")
    print("   Oe → Ö")
    print("   oe → ö")
    print("   Ue → Ü")
    print("   ue → ü")
    print()
    
    # Test double vowel patterns
    print("3. Double Vowel to ğ:")
    print("   aa → ağ")
    print("   ee → eğ")
    print("   ii → iğ")
    print("   oo → oğ")
    print("   uu → uğ")
    print()
    
    # Test place names
    print("4. Place Names:")
    print("   Istanbul → İstanbul")
    print("   Izmir → İzmir")
    print("   Diyarbakir → Diyarbakır")
    print("   Eskisehir → Eskişehir")
    print("   Elazig → Elazığ")
    print()
    
    # Test common words
    print("5. Common Words:")
    print("   teshekkuer → teşekkür")
    print("   guzel → güzel")
    print("   cok → çok")
    print("   yashayan → yaşayan")
    print("   arkadashimla → arkadaşımla")
    print()
    
    print("Run 'python test_turkish_cli.py' for interactive testing!")

if __name__ == "__main__":
    quick_test()
