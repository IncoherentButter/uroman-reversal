#!/usr/bin/env python3

"""
Python-based String Distance Testing for Reverse Uroman

This module provides string distance-based evaluation for the reverse-uroman system
using Python implementations of the cost rules from the original uroman system.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import re
from collections import defaultdict

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat
from uroman import Uroman, RomFormat


class PythonStringDistance:
    """
    Python implementation of the string distance algorithm used in uroman.
    
    This is a simplified version that implements the core functionality
    without requiring the Perl string-distance.pl script.
    """
    
    def __init__(self):
        """Initialize with basic cost rules."""
        self.cost_rules = self._load_basic_cost_rules()
    
    def _load_basic_cost_rules(self) -> Dict[str, Dict[str, float]]:
        """Load basic cost rules for character substitutions."""
        rules = defaultdict(lambda: defaultdict(float))
        
        # Basic vowel costs (very low - vowels are similar)
        for vowel in 'aeiou':
            rules[vowel][vowel] = 0.0  # Same vowel
            for other_vowel in 'aeiou':
                if other_vowel != vowel:
                    rules[vowel][other_vowel] = 0.1  # Different vowel
        
        # Consonant costs (higher - more significant differences)
        consonants = 'bcdfghjklmnpqrstvwxyz'
        for cons in consonants:
            rules[cons][cons] = 0.0  # Same consonant
            for other_cons in consonants:
                if other_cons != cons:
                    rules[cons][other_cons] = 1.0  # Different consonant
        
        # Special cases for common substitutions
        special_cases = {
            ('f', 'ph'): 0.01,  # Very similar sounds
            ('c', 'k'): 0.2,    # Common substitution
            ('c', 's'): 0.3,    # Less common
            ('g', 'j'): 0.3,    # Similar sounds
            ('b', 'p'): 0.3,    # Voiced/unvoiced
            ('d', 't'): 0.3,    # Voiced/unvoiced
            ('v', 'w'): 0.2,    # Similar sounds
            ('s', 'z'): 0.2,    # Voiced/unvoiced
            ('ch', 'sh'): 0.2,  # Digraphs
            ('th', 't'): 0.4,   # Common in some languages
            ('kh', 'k'): 0.2,   # Guttural sounds
            ('gh', 'g'): 0.2,   # Guttural sounds
        }
        
        for (from_char, to_char), cost in special_cases.items():
            rules[from_char][to_char] = cost
            rules[to_char][from_char] = cost  # Symmetric
        
        return rules
    
    def calculate_distance(self, text1: str, text2: str, debug: bool = False) -> float:
        """
        Calculate string distance between two texts.
        
        Args:
            text1: First text
            text2: Second text
            debug: Enable detailed debugging output
            
        Returns:
            Distance score (lower = more similar)
        """
        # Store original texts for debugging
        original_text1, original_text2 = text1, text2
        
        # Normalize texts
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        
        if debug:
            print(f"\n=== STRING DISTANCE DEBUG ===")
            print(f"Original text1: '{original_text1}' (len={len(original_text1)})")
            print(f"Original text2: '{original_text2}' (len={len(original_text2)})")
            print(f"Normalized text1: '{text1}' (len={len(text1)})")
            print(f"Normalized text2: '{text2}' (len={len(text2)})")
            print(f"Text1 bytes: {text1.encode('utf-8')}")
            print(f"Text2 bytes: {text2.encode('utf-8')}")
            print(f"Are they equal? {text1 == text2}")
            print(f"Character-by-character comparison:")
            for i, (c1, c2) in enumerate(zip(text1, text2)):
                match = "✓" if c1 == c2 else "✗"
                print(f"  [{i:2d}] '{c1}' vs '{c2}' {match} (bytes: {c1.encode('utf-8')} vs {c2.encode('utf-8')})")
            if len(text1) != len(text2):
                print(f"  Length difference: {len(text1)} vs {len(text2)}")
                if len(text1) > len(text2):
                    print(f"  Extra chars in text1: '{text1[len(text2):]}'")
                else:
                    print(f"  Extra chars in text2: '{text2[len(text1):]}'")
        
        # Use dynamic programming (Levenshtein distance with custom costs)
        m, n = len(text1), len(text2)
        
        if debug:
            print(f"\nMatrix dimensions: {m+1} x {n+1}")
        
        # Create distance matrix
        dp = [[0.0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i * 1.0  # Deletion cost
        for j in range(n + 1):
            dp[0][j] = j * 1.0  # Insertion cost
        
        if debug:
            print(f"\nInitialized matrix:")
            print("   ", end="")
            for j in range(n + 1):
                print(f"{j:4}", end="")
            print()
            for i in range(m + 1):
                print(f"{i:2}: ", end="")
                for j in range(n + 1):
                    print(f"{dp[i][j]:4.1f}", end="")
                print()
        
        # Fill the matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                char1, char2 = text1[i-1], text2[j-1]
                
                if debug:
                    print(f"\nPosition [{i},{j}]: comparing '{char1}' vs '{char2}'")
                
                if char1 == char2:
                    dp[i][j] = dp[i-1][j-1]  # No cost for match
                    if debug:
                        print(f"  Match! dp[{i},{j}] = dp[{i-1},{j-1}] = {dp[i][j]}")
                else:
                    # Calculate substitution cost
                    sub_cost = self._get_substitution_cost(char1, char2)
                    
                    # Calculate all three operations
                    deletion_cost = dp[i-1][j] + 1.0
                    insertion_cost = dp[i][j-1] + 1.0
                    substitution_cost = dp[i-1][j-1] + sub_cost
                    
                    # Take minimum of three operations
                    dp[i][j] = min(deletion_cost, insertion_cost, substitution_cost)
                    
                    if debug:
                        print(f"  Mismatch! Options:")
                        print(f"    Deletion:    dp[{i-1},{j}] + 1.0 = {dp[i-1][j]:.1f} + 1.0 = {deletion_cost:.1f}")
                        print(f"    Insertion:   dp[{i},{j-1}] + 1.0 = {dp[i][j-1]:.1f} + 1.0 = {insertion_cost:.1f}")
                        print(f"    Substitution: dp[{i-1},{j-1}] + {sub_cost:.1f} = {dp[i-1][j-1]:.1f} + {sub_cost:.1f} = {substitution_cost:.1f}")
                        print(f"    Chosen: {dp[i][j]:.1f} ({'deletion' if dp[i][j] == deletion_cost else 'insertion' if dp[i][j] == insertion_cost else 'substitution'})")
        
        if debug:
            print(f"\nFinal matrix:")
            print("   ", end="")
            for j in range(n + 1):
                print(f"{j:4}", end="")
            print()
            for i in range(m + 1):
                print(f"{i:2}: ", end="")
                for j in range(n + 1):
                    print(f"{dp[i][j]:4.1f}", end="")
                print()
            print(f"\nFinal distance: dp[{m},{n}] = {dp[m][n]}")
            print("=== END DEBUG ===\n")
        
        return dp[m][n]
    
    def _get_substitution_cost(self, char1: str, char2: str) -> float:
        """Get substitution cost between two characters."""
        return self.cost_rules[char1][char2] if char1 in self.cost_rules and char2 in self.cost_rules[char1] else 1.0
    
    def calculate_normalized_distance(self, text1: str, text2: str) -> float:
        """
        Calculate normalized string distance (0-1 scale).
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Normalized distance (0 = identical, 1 = completely different)
        """
        distance = self.calculate_distance(text1, text2)
        max_length = max(len(text1), len(text2))
        return distance / max_length if max_length > 0 else 0.0


class ReverseStringDistanceTester:
    """
    String distance testing for reverse-uroman system using Python implementation.
    """
    
    def __init__(self, data_dir: Path = None):
        """Initialize the tester."""
        self.data_dir = data_dir or Path(__file__).parent
        self.uroman = Uroman(data_dir=self.data_dir)
        self.reverse_uroman = ReverseUroman(data_dir=self.data_dir)
        self.string_distance = PythonStringDistance()
    
    def test_round_trip_romanization(self, 
                                   original_texts: List[str], 
                                   language_codes: List[str],
                                   target_scripts: List[str]) -> Dict[str, Any]:
        """
        Test round-trip romanization: Original → Romanized → Reverse Romanized.
        """
        results = {
            'test_type': 'round_trip',
            'samples': [],
            'summary': {}
        }
        
        total_distance = 0.0
        total_chars = 0
        successful_tests = 0
        
        for i, (original, lang_code, target_script) in enumerate(zip(original_texts, language_codes, target_scripts)):
            try:
                # Step 1: Romanize original text
                romanized = self.uroman.romanize_string(original, lcode=lang_code)
                
                # Step 2: Reverse romanize back to target script
                reverse_romanized = self.reverse_uroman.reverse_romanize_string(
                    romanized, target_script=target_script
                )
                
                # Step 3: Calculate string distance
                distance = self.string_distance.calculate_distance(original, reverse_romanized)
                normalized_distance = self.string_distance.calculate_normalized_distance(original, reverse_romanized)
                
                sample_result = {
                    'sample_id': i,
                    'original': original,
                    'romanized': romanized,
                    'reverse_romanized': reverse_romanized,
                    'language_code': lang_code,
                    'target_script': target_script,
                    'string_distance': distance,
                    'normalized_distance': normalized_distance,
                    'character_count': len(original),
                    'success': normalized_distance < 0.5  # Threshold for success
                }
                
                results['samples'].append(sample_result)
                
                if sample_result['success']:
                    successful_tests += 1
                
                total_distance += distance
                total_chars += len(original)
                
            except Exception as e:
                sample_result = {
                    'sample_id': i,
                    'original': original,
                    'error': str(e),
                    'success': False
                }
                results['samples'].append(sample_result)
        
        # Calculate summary statistics
        results['summary'] = {
            'total_samples': len(original_texts),
            'successful_samples': successful_tests,
            'success_rate': successful_tests / len(original_texts) if original_texts else 0,
            'average_distance': total_distance / len(original_texts) if original_texts else 0,
            'average_normalized_distance': total_distance / total_chars if total_chars > 0 else 0,
            'total_characters': total_chars
        }
        
        return results
    
    def test_direct_reverse_romanization(self,
                                       test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Test direct reverse romanization against known expected outputs.
        """
        results = {
            'test_type': 'direct_reverse',
            'samples': [],
            'summary': {}
        }
        
        total_distance = 0.0
        total_chars = 0
        successful_tests = 0
        
        for i, test_case in enumerate(test_cases):
            try:
                latin_input = test_case['latin']
                expected_output = test_case['expected']
                target_script = test_case['script']
                
                # Perform reverse romanization
                actual_output = self.reverse_uroman.reverse_romanize_string(
                    latin_input, target_script=target_script
                )
                
                # Calculate string distance
                distance = self.string_distance.calculate_distance(expected_output, actual_output, debug=True)
                normalized_distance = self.string_distance.calculate_normalized_distance(expected_output, actual_output)
                
                sample_result = {
                    'sample_id': i,
                    'latin_input': latin_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'target_script': target_script,
                    'string_distance': distance,
                    'normalized_distance': normalized_distance,
                    'character_count': len(expected_output),
                    'success': normalized_distance < 0.3  # Stricter threshold for direct tests
                }
                
                results['samples'].append(sample_result)
                
                if sample_result['success']:
                    successful_tests += 1
                
                total_distance += distance
                total_chars += len(expected_output)
                
            except Exception as e:
                sample_result = {
                    'sample_id': i,
                    'latin_input': test_case.get('latin', ''),
                    'error': str(e),
                    'success': False
                }
                results['samples'].append(sample_result)
        
        # Calculate summary statistics
        results['summary'] = {
            'total_samples': len(test_cases),
            'successful_samples': successful_tests,
            'success_rate': successful_tests / len(test_cases) if test_cases else 0,
            'average_distance': total_distance / len(test_cases) if test_cases else 0,
            'average_normalized_distance': total_distance / total_chars if total_chars > 0 else 0,
            'total_characters': total_chars
        }
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a detailed test report."""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("REVERSE UROMAN STRING DISTANCE TEST REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Test type and summary
        report_lines.append(f"Test Type: {results['test_type']}")
        report_lines.append("")
        
        # Summary statistics
        summary = results['summary']
        report_lines.append("SUMMARY STATISTICS")
        report_lines.append("-" * 30)
        report_lines.append(f"Total Samples: {summary['total_samples']}")
        report_lines.append(f"Successful Samples: {summary['successful_samples']}")
        report_lines.append(f"Success Rate: {summary['success_rate']:.2%}")
        report_lines.append(f"Average Distance: {summary['average_distance']:.3f}")
        report_lines.append(f"Average Normalized Distance: {summary['average_normalized_distance']:.3f}")
        report_lines.append("")
        
        # Sample details
        report_lines.append("SAMPLE DETAILS")
        report_lines.append("-" * 30)
        for sample in results['samples']:
            if 'error' in sample:
                report_lines.append(f"Sample {sample['sample_id']}: ERROR - {sample['error']}")
            else:
                report_lines.append(f"Sample {sample['sample_id']}:")
                if 'original' in sample:
                    report_lines.append(f"  Original: {sample['original']}")
                if 'latin_input' in sample:
                    report_lines.append(f"  Latin Input: {sample['latin_input']}")
                if 'expected_output' in sample:
                    report_lines.append(f"  Expected: {sample['expected_output']}")
                if 'actual_output' in sample:
                    report_lines.append(f"  Actual: {sample['actual_output']}")
                report_lines.append(f"  Distance: {sample['string_distance']:.3f}")
                report_lines.append(f"  Normalized Distance: {sample['normalized_distance']:.3f}")
                report_lines.append(f"  Success: {sample['success']}")
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main function for testing reverse-uroman with string distance metrics."""
    tester = ReverseStringDistanceTester()
    
    # Example test cases for Arabic
    arabic_test_cases = [
        {'latin': 'salam', 'expected': 'سلام', 'script': 'Arabic'},
        {'latin': 'muhammad', 'expected': 'محمد', 'script': 'Arabic'},
        {'latin': 'allah', 'expected': 'الله', 'script': 'Arabic'},
        {'latin': 'kitab', 'expected': 'كتاب', 'script': 'Arabic'},
    ]
    
    # Example test cases for Swahili
    swahili_test_cases = [
        {'latin': 'jambo', 'expected': 'jambo', 'script': 'Swahili'},
        {'latin': 'asante', 'expected': 'asante', 'script': 'Swahili'},
        {'latin': 'karibu', 'expected': 'karibu', 'script': 'Swahili'},
    ]
    
    print("Testing Reverse Uroman with String Distance Metrics (Python)")
    print("=" * 60)
    
    # Test Arabic reverse romanization
    print("\nTesting Arabic Reverse Romanization...")
    arabic_results = tester.test_direct_reverse_romanization(arabic_test_cases)
    print(tester.generate_report(arabic_results))
    
    # Test Swahili reverse romanization
    print("\nTesting Swahili Reverse Romanization...")
    swahili_results = tester.test_direct_reverse_romanization(swahili_test_cases)
    print(tester.generate_report(swahili_results))


if __name__ == "__main__":
    main()
