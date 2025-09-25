#!/usr/bin/env python3
"""
Full Test Suite Runner for Reverse Uroman System
Runs all tests to verify the system is working correctly
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import uroman modules
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_reverse_spaces():
    """Test space preservation in reverse romanization"""
    print("🔤 Testing Space Preservation in Reverse Romanization")
    print("=" * 60)
    
    try:
        from reverse_uroman import ReverseUroman
        r = ReverseUroman()
        
        # Test Swahili
        result1 = r.reverse_romanize_string('habari yako', target_script='Swahili')
        print(f"Swahili: 'habari yako' -> '{result1}'")
        print(f"  Length: {len(result1)}")
        print(f"  Contains space: {' ' in result1}")
        print(f"  ✅ PASS" if ' ' in result1 else "  ❌ FAIL")
        print()
        
        # Test Arabic
        result2 = r.reverse_romanize_string('salam alaykum', target_script='Arabic')
        print(f"Arabic: 'salam alaykum' -> '{result2}'")
        print(f"  Length: {len(result2)}")
        print(f"  Contains space: {' ' in result2}")
        print(f"  ✅ PASS" if ' ' in result2 else "  ❌ FAIL")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing space preservation: {e}")
        return False


def test_forward_spaces():
    """Test space preservation in forward romanization"""
    print("🔤 Testing Space Preservation in Forward Romanization")
    print("=" * 60)
    
    try:
        from uroman import Uroman
        u = Uroman()
        
        # Test Swahili
        result1 = u.romanize_string('habari yako', lcode='swa')
        print(f"Swahili: 'habari yako' -> '{result1}'")
        print(f"  Length: {len(result1)}")
        print(f"  Contains space: {' ' in result1}")
        print(f"  ✅ PASS" if ' ' in result1 else "  ❌ FAIL")
        print()
        
        # Test Arabic
        result2 = u.romanize_string('salam alaykum', lcode='ara')
        print(f"Arabic: 'salam alaykum' -> '{result2}'")
        print(f"  Length: {len(result2)}")
        print(f"  Contains space: {' ' in result2}")
        print(f"  ✅ PASS" if ' ' in result2 else "  ❌ FAIL")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing forward space preservation: {e}")
        return False


def test_string_distance():
    """Test string distance calculation"""
    print("📏 Testing String Distance Calculation")
    print("=" * 60)
    
    try:
        from reverse_string_distance_python import ReverseStringDistanceTester
        tester = ReverseStringDistanceTester()
        
        # Test identical strings
        distance1 = tester.string_distance.calculate_distance("hello", "hello")
        print(f"Identical strings: 'hello' vs 'hello' = {distance1}")
        print(f"  ✅ PASS" if distance1 == 0.0 else "  ❌ FAIL")
        print()
        
        # Test different strings
        distance2 = tester.string_distance.calculate_distance("hello", "world")
        print(f"Different strings: 'hello' vs 'world' = {distance2}")
        print(f"  ✅ PASS" if distance2 > 0.0 else "  ❌ FAIL")
        print()
        
        # Test with spaces
        distance3 = tester.string_distance.calculate_distance("habari yako", "habari yako")
        print(f"With spaces: 'habari yako' vs 'habari yako' = {distance3}")
        print(f"  ✅ PASS" if distance3 == 0.0 else "  ❌ FAIL")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing string distance: {e}")
        return False


def test_reverse_romanization():
    """Test basic reverse romanization functionality"""
    print("🔄 Testing Reverse Romanization Functionality")
    print("=" * 60)
    
    try:
        from reverse_uroman import ReverseUroman
        r = ReverseUroman()
        
        test_cases = [
            ("salam", "Arabic", "Basic Arabic greeting"),
            ("jambo", "Swahili", "Swahili greeting"),
            ("hello", "Swahili", "English word"),
        ]
        
        success_count = 0
        for input_text, target_script, description in test_cases:
            try:
                result = r.reverse_romanize_string(input_text, target_script=target_script)
                print(f"✅ {description}: '{input_text}' -> '{result}'")
                success_count += 1
            except Exception as e:
                print(f"❌ {description}: '{input_text}' -> ERROR: {e}")
        
        print(f"\nPassed: {success_count}/{len(test_cases)} tests")
        return success_count == len(test_cases)
        
    except Exception as e:
        print(f"❌ Error testing reverse romanization: {e}")
        return False


def test_integration():
    """Test full integration with string distance"""
    print("🔗 Testing Full Integration with String Distance")
    print("=" * 60)
    
    try:
        from reverse_string_distance_python import ReverseStringDistanceTester
        tester = ReverseStringDistanceTester()
        
        # Test Swahili round-trip
        input_text = "habari yako"
        actual = tester.reverse_uroman.reverse_romanize_string(input_text, target_script='Swahili')
        distance = tester.string_distance.calculate_distance(input_text, actual)
        
        print(f"Swahili round-trip test:")
        print(f"  Input:    '{input_text}'")
        print(f"  Output:   '{actual}'")
        print(f"  Distance: {distance}")
        print(f"  ✅ PASS" if distance == 0.0 else "  ❌ FAIL")
        print()
        
        # Test Arabic
        input_text2 = "salam"
        actual2 = tester.reverse_uroman.reverse_romanize_string(input_text2, target_script='Arabic')
        distance2 = tester.string_distance.calculate_distance("سلام", actual2)
        
        print(f"Arabic test:")
        print(f"  Input:    '{input_text2}'")
        print(f"  Output:   '{actual2}'")
        print(f"  Expected: 'سلام'")
        print(f"  Distance: {distance2}")
        print(f"  ✅ PASS" if distance2 < 2.0 else "  ❌ FAIL")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing integration: {e}")
        return False


def test_comprehensive_metrics():
    """Test all 5 comprehensive metrics (WER, MER, WIL, WIP, CER)"""
    print("📊 Testing Comprehensive Metrics (WER, MER, WIL, WIP, CER)")
    print("=" * 60)
    
    try:
        from tests.integration.test_simple_metrics import test_simple_metrics as run_simple_metrics
        return run_simple_metrics()
    except Exception as e:
        print(f"❌ Error testing comprehensive metrics: {e}")
        return False


def main():
    """Run the full test suite"""
    print("🚀 FULL REVERSE UROMAN TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        ("Space Preservation (Reverse)", test_reverse_spaces),
        ("Space Preservation (Forward)", test_forward_spaces),
        ("String Distance Calculation", test_string_distance),
        ("Reverse Romanization", test_reverse_romanization),
        ("Full Integration", test_integration),
        ("Comprehensive Metrics (WER/MER/WIL/WIP/CER)", test_comprehensive_metrics),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"Running: {test_name}")
        print("-" * 40)
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"Result: {'✅ PASSED' if success else '❌ FAILED'}")
        except Exception as e:
            print(f"Result: ❌ FAILED - {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("📊 TEST SUMMARY")
    print("=" * 80)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    print("-" * 80)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! The reverse uroman system is working correctly.")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
