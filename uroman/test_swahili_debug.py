#!/usr/bin/env python3

from reverse_string_distance_python import ReverseStringDistanceTester

def test_swahili():
    tester = ReverseStringDistanceTester()
    
    # Test Swahili case
    input_text = "habari yako"
    actual = tester.reverse_uroman.reverse_romanize_string(input_text, target_script='Swahili')
    
    print(f"Input: '{input_text}'")
    print(f"Actual output: '{actual}'")
    print(f"Expected: '{input_text}'")
    print(f"Are they equal? {actual == input_text}")
    print(f"Length comparison: {len(actual)} vs {len(input_text)}")
    
    # Calculate distance with debug
    distance = tester.string_distance.calculate_distance(input_text, actual, debug=True)
    print(f"Distance: {distance}")

if __name__ == "__main__":
    test_swahili()
