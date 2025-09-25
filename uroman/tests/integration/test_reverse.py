#!/usr/bin/env python3

"""
Test script for the Reverse Uroman system
Tests various Latin inputs and shows Arabic conversions
"""

import sys
from pathlib import Path

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from reverse_uroman import ReverseUroman


def test_basic_reverse_romanization():
    """Test basic reverse romanization functionality"""
    
    print("🔄 Basic Reverse Romanization Test")
    print("=" * 50)
    
    # Initialize the reverse uroman system
    try:
        reverse_uroman = ReverseUroman()
        print("✅ Reverse Uroman system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize reverse uroman system: {e}")
        return
    
    # Test cases: (input, expected_output, target_script, description)
    test_cases = [
        # Arabic tests
        ("salam", "سلام", "Arabic", "Basic Arabic greeting"),
        ("ahlan", "أهلا", "Arabic", "Arabic welcome"),
        ("shukran", "شكرا", "Arabic", "Arabic thank you"),
        ("ma3a", "مع", "Arabic", "Arabic 'with'"),
        ("kayf", "كيف", "Arabic", "Arabic 'how'"),
        
        # Swahili tests
        ("jambo", "jambo", "Swahili", "Swahili greeting"),
        ("habari", "habari", "Swahili", "Swahili 'news'"),
        ("asante", "asante", "Swahili", "Swahili 'thank you'"),
        ("karibu", "karibu", "Swahili", "Swahili 'welcome'"),
        
        # English tests (should pass through)
        ("hello", "hello", "Swahili", "English greeting"),
        ("world", "world", "Swahili", "English word"),
    ]
    
    print(f"\nTesting {len(test_cases)} cases...")
    print()
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, (input_text, expected, target_script, description) in enumerate(test_cases, 1):
        try:
            # Apply reverse romanization
            result = reverse_uroman.reverse_romanize_string(input_text, target_script=target_script)
            
            # Check if result matches expected (exact match)
            success = result == expected
            if success:
                success_count += 1
            
            status = "✅" if success else "❌"
            print(f"{i:2d}. {status} {description}")
            print(f"    Input:    '{input_text}'")
            print(f"    Expected: '{expected}'")
            print(f"    Actual:   '{result}'")
            if not success:
                print(f"    Script:   {target_script}")
            print()
            
        except Exception as e:
            print(f"{i:2d}. ❌ {description}")
            print(f"    Input:    '{input_text}'")
            print(f"    Error:    {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Results: {success_count}/{total_count} tests passed ({success_count/total_count*100:.1f}%)")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
    else:
        print(f"⚠️  {total_count - success_count} tests failed")


def test_script_specific_conversions():
    """Test script-specific conversion rules"""
    
    print("\n🔤 Script-Specific Conversion Test")
    print("=" * 50)
    
    try:
        reverse_uroman = ReverseUroman()
    except Exception as e:
        print(f"❌ Failed to initialize reverse uroman system: {e}")
        return
    
    # Test the same input with different target scripts
    test_input = "salam"
    scripts = ["Arabic", "Swahili", "Turkish"]
    
    print(f"Testing input '{test_input}' with different target scripts:")
    print()
    
    for script in scripts:
        try:
            result = reverse_uroman.reverse_romanize_string(test_input, target_script=script)
            print(f"  {script:8}: '{result}'")
        except Exception as e:
            print(f"  {script:8}: ERROR - {e}")


def test_space_handling():
    """Test space handling in reverse romanization"""
    
    print("\n🔤 Space Handling Test")
    print("=" * 50)
    
    try:
        reverse_uroman = ReverseUroman()
    except Exception as e:
        print(f"❌ Failed to initialize reverse uroman system: {e}")
        return
    
    # Test cases with spaces
    test_cases = [
        ("habari yako", "Swahili", "Swahili with space"),
        ("salam alaykum", "Arabic", "Arabic with space"),
        ("hello world", "Swahili", "English with space"),
    ]
    
    for input_text, target_script, description in test_cases:
        try:
            result = reverse_uroman.reverse_romanize_string(input_text, target_script=target_script)
            space_preserved = " " in result
            status = "✅" if space_preserved else "❌"
            print(f"{status} {description}")
            print(f"    Input:  '{input_text}'")
            print(f"    Output: '{result}'")
            print(f"    Spaces preserved: {space_preserved}")
            print()
        except Exception as e:
            print(f"❌ {description}")
            print(f"    Input: '{input_text}'")
            print(f"    Error: {e}")
            print()


def test_error_handling():
    """Test error handling with invalid inputs"""
    
    print("\n⚠️  Error Handling Test")
    print("=" * 50)
    
    try:
        reverse_uroman = ReverseUroman()
    except Exception as e:
        print(f"❌ Failed to initialize reverse uroman system: {e}")
        return
    
    # Test cases that might cause errors
    error_test_cases = [
        ("", "Arabic", "Empty string"),
        ("   ", "Arabic", "Whitespace only"),
        ("123", "Arabic", "Numbers only"),
        ("!@#$%", "Arabic", "Special characters only"),
        ("salam", "InvalidScript", "Invalid target script"),
    ]
    
    for input_text, target_script, description in error_test_cases:
        try:
            result = reverse_uroman.reverse_romanize_string(input_text, target_script=target_script)
            print(f"✅ {description}")
            print(f"    Input:  '{input_text}'")
            print(f"    Output: '{result}'")
            print()
        except Exception as e:
            print(f"❌ {description}")
            print(f"    Input:  '{input_text}'")
            print(f"    Error:  {e}")
            print()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test reverse uroman system")
    parser.add_argument("--basic", action="store_true", help="Run basic tests")
    parser.add_argument("--scripts", action="store_true", help="Test script-specific conversions")
    parser.add_argument("--spaces", action="store_true", help="Test space handling")
    parser.add_argument("--errors", action="store_true", help="Test error handling")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.all or (not args.basic and not args.scripts and not args.spaces and not args.errors):
        # Run all tests by default
        test_basic_reverse_romanization()
        test_script_specific_conversions()
        test_space_handling()
        test_error_handling()
    else:
        if args.basic:
            test_basic_reverse_romanization()
        if args.scripts:
            test_script_specific_conversions()
        if args.spaces:
            test_space_handling()
        if args.errors:
            test_error_handling()


if __name__ == "__main__":
    main()
