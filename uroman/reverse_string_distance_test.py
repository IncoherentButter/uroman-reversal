#!/usr/bin/env python3

"""
String Distance Testing for Reverse Uroman

This module provides string distance-based evaluation for the reverse-uroman system,
using the same sophisticated cost rules as the original uroman system.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import subprocess
import tempfile

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat
from uroman import Uroman, RomFormat


class ReverseStringDistanceTester:
    """
    String distance testing for reverse-uroman system.
    
    This class provides comprehensive testing using the same string distance
    metrics used for forward uroman evaluation.
    """
    
    def __init__(self, data_dir: Path = None):
        """Initialize the tester with uroman and reverse-uroman instances."""
        self.data_dir = data_dir or Path(__file__).parent
        self.uroman = Uroman(data_dir=self.data_dir)
        self.reverse_uroman = ReverseUroman(data_dir=self.data_dir)
        
        # String distance script path
        self.string_distance_script = self.data_dir / "string-distance.pl"
        self.cost_rules_file = self.data_dir / "data-aux" / "string-distance-cost-rules.txt"
        
    def calculate_string_distance(self, text1: str, text2: str, 
                                lang1: str = "eng", lang2: str = "eng") -> float:
        """
        Calculate string distance using the Perl string-distance.pl script.
        
        Args:
            text1: First text for comparison
            text2: Second text for comparison
            lang1: Language code for first text
            lang2: Language code for second text
            
        Returns:
            String distance score (lower = more similar)
        """
        if not self.string_distance_script.exists():
            raise FileNotFoundError(f"String distance script not found: {self.string_distance_script}")
        
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
            f.write(f"{text1}\t{text2}\n")
            input_file = f.name
        
        try:
            # Run string distance script
            cmd = [
                "perl", str(self.string_distance_script),
                "-lc1", lang1,
                "-lc2", lang2,
                input_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                raise RuntimeError(f"String distance calculation failed: {result.stderr}")
            
            # Parse output
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith('#'):
                    continue
                parts = line.split('\t')
                if len(parts) >= 3:
                    return float(parts[2])
            
            return 99.99  # Default high distance if parsing fails
            
        finally:
            # Clean up temporary file
            os.unlink(input_file)
    
    def test_round_trip_romanization(self, 
                                   original_texts: List[str], 
                                   language_codes: List[str],
                                   target_scripts: List[str]) -> Dict[str, Any]:
        """
        Test round-trip romanization: Original → Romanized → Reverse Romanized.
        
        Args:
            original_texts: List of original non-Latin texts
            language_codes: List of language codes for romanization
            target_scripts: List of target scripts for reverse romanization
            
        Returns:
            Dictionary containing test results and metrics
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
                distance = self.calculate_string_distance(
                    original, reverse_romanized, lang_code, lang_code
                )
                
                # Calculate character-level metrics
                char_count = len(original)
                normalized_distance = distance / char_count if char_count > 0 else 1.0
                
                sample_result = {
                    'sample_id': i,
                    'original': original,
                    'romanized': romanized,
                    'reverse_romanized': reverse_romanized,
                    'language_code': lang_code,
                    'target_script': target_script,
                    'string_distance': distance,
                    'normalized_distance': normalized_distance,
                    'character_count': char_count,
                    'success': normalized_distance < 0.5  # Threshold for success
                }
                
                results['samples'].append(sample_result)
                
                if sample_result['success']:
                    successful_tests += 1
                
                total_distance += distance
                total_chars += char_count
                
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
        
        Args:
            test_cases: List of dictionaries with 'latin', 'expected', 'script' keys
            
        Returns:
            Dictionary containing test results and metrics
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
                distance = self.calculate_string_distance(
                    expected_output, actual_output, "eng", "eng"
                )
                
                # Calculate character-level metrics
                char_count = len(expected_output)
                normalized_distance = distance / char_count if char_count > 0 else 1.0
                
                sample_result = {
                    'sample_id': i,
                    'latin_input': latin_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'target_script': target_script,
                    'string_distance': distance,
                    'normalized_distance': normalized_distance,
                    'character_count': char_count,
                    'success': normalized_distance < 0.3  # Stricter threshold for direct tests
                }
                
                results['samples'].append(sample_result)
                
                if sample_result['success']:
                    successful_tests += 1
                
                total_distance += distance
                total_chars += char_count
                
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
    
    def test_script_specific_accuracy(self, 
                                    script: str, 
                                    test_cases: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Test accuracy for a specific script with detailed analysis.
        
        Args:
            script: Target script name (e.g., 'Arabic', 'Swahili')
            test_cases: List of test cases for this script
            
        Returns:
            Detailed results for the specific script
        """
        results = {
            'script': script,
            'test_type': 'script_specific',
            'samples': [],
            'error_analysis': {},
            'summary': {}
        }
        
        # Track different types of errors
        error_types = {
            'character_substitution': 0,
            'character_insertion': 0,
            'character_deletion': 0,
            'word_boundary_errors': 0,
            'diacritic_errors': 0
        }
        
        total_distance = 0.0
        successful_tests = 0
        
        for i, test_case in enumerate(test_cases):
            try:
                latin_input = test_case['latin']
                expected_output = test_case['expected']
                
                # Perform reverse romanization
                actual_output = self.reverse_uroman.reverse_romanize_string(
                    latin_input, target_script=script
                )
                
                # Calculate string distance
                distance = self.calculate_string_distance(
                    expected_output, actual_output, "eng", "eng"
                )
                
                # Analyze error types (simplified)
                char_count = len(expected_output)
                normalized_distance = distance / char_count if char_count > 0 else 1.0
                
                # Basic error type analysis
                if normalized_distance > 0.1:
                    if len(actual_output) > len(expected_output):
                        error_types['character_insertion'] += 1
                    elif len(actual_output) < len(expected_output):
                        error_types['character_deletion'] += 1
                    else:
                        error_types['character_substitution'] += 1
                
                sample_result = {
                    'sample_id': i,
                    'latin_input': latin_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'string_distance': distance,
                    'normalized_distance': normalized_distance,
                    'success': normalized_distance < 0.2,
                    'error_type': self._classify_error_type(expected_output, actual_output)
                }
                
                results['samples'].append(sample_result)
                
                if sample_result['success']:
                    successful_tests += 1
                
                total_distance += distance
                
            except Exception as e:
                sample_result = {
                    'sample_id': i,
                    'latin_input': test_case.get('latin', ''),
                    'error': str(e),
                    'success': False
                }
                results['samples'].append(sample_result)
        
        results['error_analysis'] = error_types
        results['summary'] = {
            'total_samples': len(test_cases),
            'successful_samples': successful_tests,
            'success_rate': successful_tests / len(test_cases) if test_cases else 0,
            'average_distance': total_distance / len(test_cases) if test_cases else 0,
            'script': script
        }
        
        return results
    
    def _classify_error_type(self, expected: str, actual: str) -> str:
        """Classify the type of error between expected and actual output."""
        if len(actual) > len(expected):
            return "insertion"
        elif len(actual) < len(expected):
            return "deletion"
        else:
            return "substitution"
    
    def generate_report(self, results: Dict[str, Any], output_file: Path = None) -> str:
        """
        Generate a detailed test report.
        
        Args:
            results: Test results dictionary
            output_file: Optional output file path
            
        Returns:
            Formatted report string
        """
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("REVERSE UROMAN STRING DISTANCE TEST REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Test type and summary
        report_lines.append(f"Test Type: {results['test_type']}")
        if 'script' in results:
            report_lines.append(f"Script: {results['script']}")
        report_lines.append("")
        
        # Summary statistics
        summary = results['summary']
        report_lines.append("SUMMARY STATISTICS")
        report_lines.append("-" * 30)
        report_lines.append(f"Total Samples: {summary['total_samples']}")
        report_lines.append(f"Successful Samples: {summary['successful_samples']}")
        report_lines.append(f"Success Rate: {summary['success_rate']:.2%}")
        report_lines.append(f"Average Distance: {summary['average_distance']:.3f}")
        if 'average_normalized_distance' in summary:
            report_lines.append(f"Average Normalized Distance: {summary['average_normalized_distance']:.3f}")
        report_lines.append("")
        
        # Error analysis (if available)
        if 'error_analysis' in results:
            report_lines.append("ERROR ANALYSIS")
            report_lines.append("-" * 30)
            for error_type, count in results['error_analysis'].items():
                report_lines.append(f"{error_type.replace('_', ' ').title()}: {count}")
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
                report_lines.append(f"  Success: {sample['success']}")
                report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text


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
    
    print("Testing Reverse Uroman with String Distance Metrics")
    print("=" * 50)
    
    # Test Arabic reverse romanization
    print("\nTesting Arabic Reverse Romanization...")
    arabic_results = tester.test_script_specific_accuracy('Arabic', arabic_test_cases)
    print(tester.generate_report(arabic_results))
    
    # Test Swahili reverse romanization
    print("\nTesting Swahili Reverse Romanization...")
    swahili_results = tester.test_script_specific_accuracy('Swahili', swahili_test_cases)
    print(tester.generate_report(swahili_results))


if __name__ == "__main__":
    main()
