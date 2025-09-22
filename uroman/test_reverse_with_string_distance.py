#!/usr/bin/env python3

"""
Comprehensive Test Suite for Reverse Uroman with String Distance Metrics

This script demonstrates how to use string distance metrics to evaluate
the quality of reverse romanization in the uroman system.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import json

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from reverse_string_distance_python import ReverseStringDistanceTester


def create_test_datasets() -> Dict[str, List[Dict[str, str]]]:
    """Create comprehensive test datasets for different scripts."""
    
    datasets = {
        'arabic': [
            # Basic Arabic words
            {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
            {'latin': 'muhammad', 'expected': 'محمد', 'script': 'Arabic'},
            {'latin': 'allah', 'expected': 'الله', 'script': 'Arabic'},
            {'latin': 'kitab', 'expected': 'كتاب', 'script': 'Arabic'},
            {'latin': 'bayt', 'expected': 'بيت', 'script': 'Arabic'},
            {'latin': 'rajul', 'expected': 'رجل', 'script': 'Arabic'},
            {'latin': 'imraa', 'expected': 'امرأة', 'script': 'Arabic'},
            {'latin': 'walad', 'expected': 'ولد', 'script': 'Arabic'},
            {'latin': 'bint', 'expected': 'بنت', 'script': 'Arabic'},
            {'latin': 'qamar', 'expected': 'قمر', 'script': 'Arabic'},
        ],
        
        'swahili': [
            # Swahili words (mostly same as Latin)
            {'latin': 'jambo', 'expected': 'jambo', 'script': 'Swahili'},
            {'latin': 'asante', 'expected': 'asante', 'script': 'Swahili'},
            {'latin': 'karibu', 'expected': 'karibu', 'script': 'Swahili'},
            {'latin': 'habari', 'expected': 'habari', 'script': 'Swahili'},
            {'latin': 'mzuri', 'expected': 'mzuri', 'script': 'Swahili'},
            {'latin': 'rafiki', 'expected': 'rafiki', 'script': 'Swahili'},
            {'latin': 'nyumba', 'expected': 'nyumba', 'script': 'Swahili'},
            {'latin': 'maji', 'expected': 'maji', 'script': 'Swahili'},
            {'latin': 'chakula', 'expected': 'chakula', 'script': 'Swahili'},
            {'latin': 'safari', 'expected': 'safari', 'script': 'Swahili'},
        ],
        
        'round_trip_arabic': [
            # For round-trip testing: Arabic → Romanized → Reverse Romanized
            {'original': 'السلام عليكم', 'lang_code': 'ara', 'target_script': 'Arabic'},
            {'original': 'أهلاً وسهلاً', 'lang_code': 'ara', 'target_script': 'Arabic'},
            {'original': 'كيف حالك', 'lang_code': 'ara', 'target_script': 'Arabic'},
            {'original': 'شكراً لك', 'lang_code': 'ara', 'target_script': 'Arabic'},
            {'original': 'مع السلامة', 'lang_code': 'ara', 'target_script': 'Arabic'},
        ],
        
        'round_trip_swahili': [
            # For round-trip testing: Swahili → Romanized → Reverse Romanized
            {'original': 'hujambo', 'lang_code': 'swa', 'target_script': 'Swahili'},
            {'original': 'sijambo', 'lang_code': 'swa', 'target_script': 'Swahili'},
            {'original': 'habari yako', 'lang_code': 'swa', 'target_script': 'Swahili'},
            {'original': 'nzuri sana', 'lang_code': 'swa', 'target_script': 'Swahili'},
            {'original': 'asante sana', 'lang_code': 'swa', 'target_script': 'Swahili'},
        ]
    }
    
    return datasets


def run_comprehensive_tests():
    """Run comprehensive tests for reverse-uroman with string distance metrics."""
    
    print("=" * 80)
    print("COMPREHENSIVE REVERSE UROMAN STRING DISTANCE TESTING")
    print("=" * 80)
    print()
    
    # Initialize tester
    tester = ReverseStringDistanceTester()
    
    # Load test datasets
    datasets = create_test_datasets()
    
    # Test 1: Direct Arabic Reverse Romanization
    print("TEST 1: Direct Arabic Reverse Romanization")
    print("-" * 50)
    arabic_results = tester.test_direct_reverse_romanization(datasets['arabic'])
    print(tester.generate_report(arabic_results))
    print()
    
    # Test 2: Direct Swahili Reverse Romanization
    print("TEST 2: Direct Swahili Reverse Romanization")
    print("-" * 50)
    swahili_results = tester.test_direct_reverse_romanization(datasets['swahili'])
    print(tester.generate_report(swahili_results))
    print()
    
    # Test 3: Round-trip Arabic Testing
    print("TEST 3: Round-trip Arabic Testing")
    print("-" * 50)
    arabic_round_trip = tester.test_round_trip_romanization(
        [item['original'] for item in datasets['round_trip_arabic']],
        [item['lang_code'] for item in datasets['round_trip_arabic']],
        [item['target_script'] for item in datasets['round_trip_arabic']]
    )
    print(tester.generate_report(arabic_round_trip))
    print()
    
    # Test 4: Round-trip Swahili Testing
    print("TEST 4: Round-trip Swahili Testing")
    print("-" * 50)
    swahili_round_trip = tester.test_round_trip_romanization(
        [item['original'] for item in datasets['round_trip_swahili']],
        [item['lang_code'] for item in datasets['round_trip_swahili']],
        [item['target_script'] for item in datasets['round_trip_swahili']]
    )
    print(tester.generate_report(swahili_round_trip))
    print()
    
    # Summary Report
    print("OVERALL SUMMARY")
    print("=" * 50)
    
    all_results = [
        ("Arabic Direct", arabic_results),
        ("Swahili Direct", swahili_results),
        ("Arabic Round-trip", arabic_round_trip),
        ("Swahili Round-trip", swahili_round_trip)
    ]
    
    for test_name, results in all_results:
        summary = results['summary']
        print(f"{test_name:20} | Success: {summary['success_rate']:6.1%} | "
              f"Avg Distance: {summary['average_distance']:6.2f} | "
              f"Norm Distance: {summary['average_normalized_distance']:6.3f}")
    
    print()
    print("=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)


def run_quick_demo():
    """Run a quick demonstration of the string distance testing."""
    
    print("QUICK DEMO: Reverse Uroman String Distance Testing")
    print("=" * 60)
    print()
    
    tester = ReverseStringDistanceTester()
    
    # Simple test cases
    test_cases = [
        {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
        {'latin': 'jambo', 'expected': 'jambo', 'script': 'Swahili'},
        {'latin': 'hello', 'expected': 'hello', 'script': 'Swahili'},
    ]
    
    print("Testing individual cases:")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases):
        try:
            latin_input = test_case['latin']
            expected = test_case['expected']
            script = test_case['script']
            
            # Perform reverse romanization
            actual = tester.reverse_uroman.reverse_romanize_string(latin_input, target_script=script)
            
            # Calculate distance
            distance = tester.string_distance.calculate_distance(expected, actual)
            normalized = tester.string_distance.calculate_normalized_distance(expected, actual)
            
            print(f"Test {i+1}:")
            print(f"  Input:     {latin_input}")
            print(f"  Expected:  {expected}")
            print(f"  Actual:    {actual}")
            print(f"  Distance:  {distance:.3f}")
            print(f"  Normalized: {normalized:.3f}")
            print(f"  Success:   {normalized < 0.3}")
            print()
            
        except Exception as e:
            print(f"Test {i+1} failed: {e}")
            print()


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test reverse-uroman with string distance metrics")
    parser.add_argument("--demo", action="store_true", help="Run quick demo")
    parser.add_argument("--full", action="store_true", help="Run comprehensive tests")
    
    args = parser.parse_args()
    
    if args.demo:
        run_quick_demo()
    elif args.full:
        run_comprehensive_tests()
    else:
        print("Please specify --demo or --full")
        print("  --demo: Run quick demonstration")
        print("  --full: Run comprehensive test suite")


if __name__ == "__main__":
    main()
