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
sys.path.insert(0, str(Path(__file__).parent.parent))

from reverse_string_distance_python import ReverseStringDistanceTester


class ReverseUromanTester:
    """Main test class for reverse uroman with string distance evaluation"""
    
    def __init__(self):
        """Initialize the tester with reverse uroman and string distance components"""
        self.reverse_uroman = None
        self.string_distance = None
        self.test_cases = []
        
    def setup(self):
        """Set up the reverse uroman and string distance components"""
        try:
            from reverse_uroman import ReverseUroman
            from reverse_string_distance_python import ReverseStringDistanceTester
            
            self.reverse_uroman = ReverseUroman()
            self.string_distance = ReverseStringDistanceTester()
            
            print("✅ Successfully initialized reverse uroman and string distance components")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize components: {e}")
            return False
    
    def add_test_case(self, input_text: str, expected_output: str, 
                     target_script: str, description: str = ""):
        """Add a test case to the test suite"""
        self.test_cases.append({
            'input': input_text,
            'expected': expected_output,
            'target_script': target_script,
            'description': description
        })
    
    def load_sample_test_cases(self):
        """Load some sample test cases for demonstration"""
        # Arabic test cases
        self.add_test_case("salam", "سلام", "Arabic", "Basic Arabic greeting")
        self.add_test_case("ahlan", "أهلا", "Arabic", "Arabic welcome")
        
        # Swahili test cases  
        self.add_test_case("jambo", "jambo", "Swahili", "Swahili greeting")
        self.add_test_case("habari", "habari", "Swahili", "Swahili 'how are you'")
        
        # English test cases (should pass through unchanged)
        self.add_test_case("hello", "hello", "Swahili", "English greeting")
        self.add_test_case("world", "world", "Swahili", "English word")
    
    def run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case and return results"""
        try:
            # Get actual output from reverse romanization
            actual = self.reverse_uroman.reverse_romanize_string(
                test_case['input'], 
                target_script=test_case['target_script']
            )
            
            # Calculate string distance metrics
            distance = self.string_distance.calculate_distance(
                test_case['expected'], 
                actual
            )
            normalized_distance = self.string_distance.calculate_normalized_distance(
                test_case['expected'], 
                actual
            )
            
            # Determine success (distance < 1.0 is considered successful)
            success = distance < 1.0
            
            return {
                'input': test_case['input'],
                'expected': test_case['expected'],
                'actual': actual,
                'target_script': test_case['target_script'],
                'description': test_case['description'],
                'distance': round(distance, 3),
                'normalized_distance': round(normalized_distance, 3),
                'success': success,
                'error': None
            }
            
        except Exception as e:
            return {
                'input': test_case['input'],
                'expected': test_case['expected'],
                'actual': None,
                'target_script': test_case['target_script'],
                'description': test_case['description'],
                'distance': float('inf'),
                'normalized_distance': 1.0,
                'success': False,
                'error': str(e)
            }
    
    def run_all_tests(self) -> List[Dict[str, Any]]:
        """Run all test cases and return results"""
        if not self.reverse_uroman or not self.string_distance:
            print("❌ Components not initialized. Call setup() first.")
            return []
        
        results = []
        print(f"\n🧪 Running {len(self.test_cases)} test cases...")
        print("=" * 60)
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\nTest {i}: {test_case['description']}")
            print(f"  Input:     {test_case['input']}")
            print(f"  Expected:  {test_case['expected']}")
            
            result = self.run_single_test(test_case)
            results.append(result)
            
            if result['error']:
                print(f"  ❌ Error:   {result['error']}")
            else:
                print(f"  Actual:    {result['actual']}")
                print(f"  Distance:  {result['distance']:.3f}")
                print(f"  Normalized: {result['normalized_distance']:.3f}")
                print(f"  Success:   {'✅' if result['success'] else '❌'}")
        
        return results
    
    def print_summary(self, results: List[Dict[str, Any]]):
        """Print a summary of test results"""
        if not results:
            print("No results to summarize.")
            return
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"\n📊 TEST SUMMARY")
        print("=" * 40)
        print(f"Total tests:    {total_tests}")
        print(f"Successful:     {successful_tests} ✅")
        print(f"Failed:         {failed_tests} ❌")
        print(f"Success rate:   {successful_tests/total_tests*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed tests:")
            for result in results:
                if not result['success']:
                    print(f"  - {result['input']} -> {result['actual']} (expected: {result['expected']})")
    
    def save_results(self, results: List[Dict[str, Any]], filename: str = "test_results.json"):
        """Save test results to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")


def run_quick_demo():
    """Run a quick demonstration of the testing system"""
    print("🚀 QUICK DEMO: Reverse Uroman String Distance Testing")
    print("=" * 60)
    
    # Initialize tester
    tester = ReverseUromanTester()
    if not tester.setup():
        return
    
    # Load sample test cases
    tester.load_sample_test_cases()
    
    # Run tests
    results = tester.run_all_tests()
    
    # Print summary
    tester.print_summary(results)
    
    # Save results
    tester.save_results(results, "quick_demo_results.json")


def main():
    """Main function with command line argument handling"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test reverse uroman with string distance metrics")
    parser.add_argument("--demo", action="store_true", help="Run quick demonstration")
    parser.add_argument("--input", type=str, help="Test specific input text")
    parser.add_argument("--expected", type=str, help="Expected output text")
    parser.add_argument("--script", type=str, default="Arabic", help="Target script (default: Arabic)")
    parser.add_argument("--output", type=str, help="Output file for results")
    
    args = parser.parse_args()
    
    if args.demo:
        run_quick_demo()
    elif args.input and args.expected:
        # Test specific case
        tester = ReverseUromanTester()
        if tester.setup():
            tester.add_test_case(args.input, args.expected, args.script, "Custom test")
            results = tester.run_all_tests()
            tester.print_summary(results)
            if args.output:
                tester.save_results(results, args.output)
    else:
        # Run full test suite
        tester = ReverseUromanTester()
        if tester.setup():
            tester.load_sample_test_cases()
            results = tester.run_all_tests()
            tester.print_summary(results)
            tester.save_results(results)


if __name__ == "__main__":
    main()
