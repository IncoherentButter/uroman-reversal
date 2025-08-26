#!/usr/bin/env python3

"""
Test script for the Reverse Uroman system
Tests various Latin inputs and shows Arabic conversions
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import reverse_uroman
sys.path.append(str(Path(__file__).parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat

def test_basic_conversions():
    """Test basic Latin to Arabic conversions"""
    print("=== Testing Basic Conversions ===")
    
    # Create reverse uroman instance
    reverse_uroman = ReverseUroman()
    
    # Test basic words
    test_words = [
        "hello",
        "world",
        "salam",
        "muhammad",
        "allah",
        "shukran",
        "marhaba"
    ]
    
    for word in test_words:
        result = reverse_uroman.reverse_romanize_string(word, target_script="Arabic")
        print(f"{word:15} → {result}")
    
    print()

def test_sentences():
    """Test sentence-level conversions"""
    print("=== Testing Sentences ===")
    
    reverse_uroman = ReverseUroman()
    
    test_sentences = [
        "hello world",
        "salam alaikum",
        "muhammad ali",
        "thank you very much",
        "peace be upon you"
    ]
    
    for sentence in test_sentences:
        result = reverse_uroman.reverse_romanize_string(sentence, target_script="Arabic")
        print(f"'{sentence}' → '{result}'")
    
    print()

def test_different_formats():
    """Test different output formats"""
    print("=== Testing Different Output Formats ===")
    
    reverse_uroman = ReverseUroman()
    test_text = "hello world"
    
    # String format
    str_result = reverse_uroman.reverse_romanize_string(
        test_text, target_script="Arabic", format=ReverseRomFormat.STR
    )
    print(f"String format: {str_result}")
    
    # Edges format
    edges_result = reverse_uroman.reverse_romanize_string(
        test_text, target_script="Arabic", format=ReverseRomFormat.EDGES
    )
    print(f"Edges format: {len(edges_result)} edges")
    for edge in edges_result:
        print(f"  {edge}")
    
    # Lattice format
    lattice_result = reverse_uroman.reverse_romanize_string(
        test_text, target_script="Arabic", format=ReverseRomFormat.LATTICE
    )
    print(f"Lattice format: {len(lattice_result)} total edges")
    
    print()

def test_priority_system():
    """Test the priority system for rule selection"""
    print("=== Testing Priority System ===")
    
    reverse_uroman = ReverseUroman()
    
    # Test words that have multiple possible mappings
    test_words = [
        "sh",      # Should prefer ش (priority 200) over s+h (priority 100)
        "th",      # Should prefer ث (priority 200) over t+h (priority 100)
        "kh",      # Should prefer خ (priority 200) over k+h (priority 100)
        "ng",      # Should prefer نغ (priority 150) over n+g (priority 100)
    ]
    
    for word in test_words:
        result = reverse_uroman.reverse_romanize_string(word, target_script="Arabic")
        print(f"{word:5} → {result}")
    
    print()

def test_fallback_mapping():
    """Test fallback mapping for unknown words"""
    print("=== Testing Fallback Mapping ===")
    
    reverse_uroman = ReverseUroman()
    
    # Test words that aren't in our rules
    test_words = [
        "xyz",     # Should use fallback mapping
        "qwerty",  # Should use fallback mapping
        "asdf",    # Should use fallback mapping
    ]
    
    for word in test_words:
        result = reverse_uroman.reverse_romanize_string(word, target_script="Arabic")
        print(f"{word:10} → {result}")
    
    print()

def test_script_switching():
    """Test switching between different target scripts"""
    print("=== Testing Script Switching ===")
    
    reverse_uroman = ReverseUroman()
    test_text = "hello world"
    
    # Test Arabic
    arabic_result = reverse_uroman.reverse_romanize_string(test_text, target_script="Arabic")
    print(f"Arabic: {arabic_result}")
    
    # Test Devanagari (should fall back to basic mapping)
    devanagari_result = reverse_uroman.reverse_romanize_string(test_text, target_script="Devanagari")
    print(f"Devanagari: {devanagari_result}")
    
    print()

def main():
    """Run all tests"""
    print("Reverse Uroman Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_basic_conversions()
        test_sentences()
        test_different_formats()
        test_priority_system()
        test_fallback_mapping()
        test_script_switching()
        
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
