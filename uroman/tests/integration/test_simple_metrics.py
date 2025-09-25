#!/usr/bin/env python3

"""
Simple Metrics Test Suite for Reverse Uroman

This script tests all 5 key metrics without external dependencies:
- Word Error Rate (WER)
- Match Error Rate (MER) 
- Word Information Lost (WIL)
- Word Information Preserved (WIP)
- Character Error Rate (CER)
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
import json
import math
from collections import Counter

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat


class SimpleMetricsCalculator:
    """Simple implementation of all 5 metrics without external dependencies"""
    
    def __init__(self):
        self.name = "Simple Metrics Calculator"
    
    def calculate_wer(self, reference_texts: List[str], hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate Word Error Rate"""
        total_wer = 0.0
        total_words = 0
        individual_wer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = ref.split()
            hyp_words = hyp.split()
            
            if len(ref_words) > 0:
                # Simple Levenshtein distance for words
                distance = self._levenshtein_distance(ref_words, hyp_words)
                sample_wer = distance / len(ref_words)
                individual_wer.append(sample_wer)
                total_wer += distance
                total_words += len(ref_words)
            else:
                individual_wer.append(0.0)
        
        overall_wer = total_wer / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wer': overall_wer,
            'individual_wer': individual_wer,
            'total_words': total_words,
            'total_edits': total_wer
        }
    
    def calculate_cer(self, reference_texts: List[str], hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate Character Error Rate"""
        total_cer = 0.0
        total_chars = 0
        individual_cer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            if len(ref) > 0:
                distance = self._levenshtein_distance(list(ref), list(hyp))
                sample_cer = distance / len(ref)
                individual_cer.append(sample_cer)
                total_cer += distance
                total_chars += len(ref)
            else:
                individual_cer.append(0.0)
        
        overall_cer = total_cer / total_chars if total_chars > 0 else 0.0
        
        return {
            'overall_cer': overall_cer,
            'individual_cer': individual_cer,
            'total_chars': total_chars,
            'total_edits': total_cer
        }
    
    def calculate_mer(self, reference_texts: List[str], hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate Match Error Rate"""
        total_mer = 0.0
        total_words = 0
        individual_mer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = ref.split()
            hyp_words = hyp.split()
            
            if len(ref_words) > 0:
                matches = sum(1 for r, h in zip(ref_words, hyp_words) if r == h)
                sample_mer = (len(ref_words) - matches) / len(ref_words)
                individual_mer.append(sample_mer)
                total_mer += (len(ref_words) - matches)
                total_words += len(ref_words)
            else:
                individual_mer.append(0.0)
        
        overall_mer = total_mer / total_words if total_words > 0 else 0.0
        
        return {
            'overall_mer': overall_mer,
            'individual_mer': individual_mer,
            'total_words': total_words,
            'total_mismatches': total_mer
        }
    
    def calculate_wil(self, reference_texts: List[str], hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate Word Information Lost"""
        total_wil = 0.0
        total_words = 0
        individual_wil = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = ref.split()
            hyp_words = hyp.split()
            
            if len(ref_words) > 0:
                ref_info = self._calculate_word_information_content(ref_words)
                hyp_info = self._calculate_word_information_content(hyp_words)
                sample_wil = max(0.0, (ref_info - hyp_info) / ref_info) if ref_info > 0 else 0.0
                individual_wil.append(sample_wil)
                total_wil += sample_wil * len(ref_words)
                total_words += len(ref_words)
            else:
                individual_wil.append(0.0)
        
        overall_wil = total_wil / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wil': overall_wil,
            'individual_wil': individual_wil,
            'total_words': total_words,
            'total_information_lost': total_wil
        }
    
    def calculate_wip(self, reference_texts: List[str], hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate Word Information Preserved"""
        total_wip = 0.0
        total_words = 0
        individual_wip = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = ref.split()
            hyp_words = hyp.split()
            
            if len(ref_words) > 0:
                ref_info = self._calculate_word_information_content(ref_words)
                hyp_info = self._calculate_word_information_content(hyp_words)
                sample_wip = min(hyp_info / ref_info, 1.0) if ref_info > 0 else 0.0
                individual_wip.append(sample_wip)
                total_wip += sample_wip * len(ref_words)
                total_words += len(ref_words)
            else:
                individual_wip.append(0.0)
        
        overall_wip = total_wip / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wip': overall_wip,
            'individual_wip': individual_wip,
            'total_words': total_words,
            'total_information_preserved': total_wip
        }
    
    def _levenshtein_distance(self, seq1, seq2):
        """Calculate Levenshtein distance between two sequences"""
        if len(seq1) < len(seq2):
            return self._levenshtein_distance(seq2, seq1)
        
        if len(seq2) == 0:
            return len(seq1)
        
        previous_row = list(range(len(seq2) + 1))
        for i, c1 in enumerate(seq1):
            current_row = [i + 1]
            for j, c2 in enumerate(seq2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def _calculate_word_information_content(self, words: List[str]) -> float:
        """Calculate information content of a list of words"""
        if not words:
            return 0.0
        
        word_counts = Counter(words)
        total_words = len(words)
        
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy * total_words


class SimpleMetricsTester:
    """Test class for simple metrics evaluation"""
    
    def __init__(self):
        """Initialize the simple metrics tester"""
        self.reverse_uroman = None
        self.metrics_calculator = SimpleMetricsCalculator()
        self.test_cases = []
        
    def setup(self):
        """Set up the reverse uroman and metrics calculator"""
        try:
            self.reverse_uroman = ReverseUroman()
            print("✅ Successfully initialized reverse uroman and metrics calculator")
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
    
    def run_comprehensive_evaluation(self) -> Dict[str, Any]:
        """Run comprehensive evaluation with all 5 metrics"""
        if not self.test_cases:
            print("❌ No test cases available")
            return {}
        
        print("🔍 Running Simple Metrics Evaluation")
        print("=" * 50)
        
        # Prepare data for metrics
        reference_texts = []
        hypothesis_texts = []
        test_results = []
        
        for i, test_case in enumerate(self.test_cases, 1):
            print(f"\n📝 Test Case {i}: {test_case['description']}")
            print(f"   Input: '{test_case['input']}'")
            print(f"   Expected: '{test_case['expected']}'")
            
            try:
                # Perform reverse romanization
                result = self.reverse_uroman.reverse_romanize_string(
                    test_case['input'], 
                    test_case['target_script']
                )
                
                print(f"   Output: '{result}'")
                
                # Store for metrics calculation
                reference_texts.append(test_case['expected'])
                hypothesis_texts.append(result)
                
                test_results.append({
                    'test_case': i,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'output': result,
                    'target_script': test_case['target_script'],
                    'description': test_case['description']
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        if not reference_texts:
            print("❌ No successful test cases for metrics calculation")
            return {}
        
        print(f"\n📊 Calculating All 5 Metrics on {len(reference_texts)} test cases")
        print("-" * 50)
        
        # Calculate all metrics
        metrics_results = {}
        
        print("   Calculating WER...")
        metrics_results['WER'] = self.metrics_calculator.calculate_wer(reference_texts, hypothesis_texts)
        
        print("   Calculating CER...")
        metrics_results['CER'] = self.metrics_calculator.calculate_cer(reference_texts, hypothesis_texts)
        
        print("   Calculating MER...")
        metrics_results['MER'] = self.metrics_calculator.calculate_mer(reference_texts, hypothesis_texts)
        
        print("   Calculating WIL...")
        metrics_results['WIL'] = self.metrics_calculator.calculate_wil(reference_texts, hypothesis_texts)
        
        print("   Calculating WIP...")
        metrics_results['WIP'] = self.metrics_calculator.calculate_wip(reference_texts, hypothesis_texts)
        
        return {
            'test_results': test_results,
            'metrics_results': metrics_results,
            'summary': self._generate_summary(metrics_results)
        }
    
    def _generate_summary(self, metrics_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of all metrics"""
        summary = {
            'total_tests': len(self.test_cases),
            'successful_tests': len([r for r in metrics_results.values() if 'error' not in r]),
            'metrics_summary': {}
        }
        
        for metric_name, result in metrics_results.items():
            if 'error' not in result:
                overall_key = f'overall_{metric_name.lower()}'
                if overall_key in result:
                    summary['metrics_summary'][metric_name] = {
                        'value': result[overall_key],
                        'status': '✅ Calculated'
                    }
                else:
                    summary['metrics_summary'][metric_name] = {
                        'value': 'N/A',
                        'status': '⚠️ No overall value'
                    }
            else:
                summary['metrics_summary'][metric_name] = {
                    'value': 'N/A',
                    'status': f'❌ Error: {result["error"]}'
                }
        
        return summary
    
    def print_detailed_results(self, results: Dict[str, Any]):
        """Print detailed results for all metrics"""
        if not results:
            print("❌ No results to display")
            return
        
        print("\n" + "=" * 70)
        print("📊 SIMPLE METRICS RESULTS")
        print("=" * 70)
        
        # Print test results
        print(f"\n🧪 Test Results: {results['summary']['total_tests']} total, {results['summary']['successful_tests']} successful")
        print("-" * 40)
        
        for test_result in results['test_results']:
            print(f"Test {test_result['test_case']}: {test_result['description']}")
            print(f"  Input:    '{test_result['input']}'")
            print(f"  Expected: '{test_result['expected']}'")
            print(f"  Output:   '{test_result['output']}'")
            print()
        
        # Print metrics summary
        print("📈 Metrics Summary:")
        print("-" * 40)
        for metric_name, metric_data in results['summary']['metrics_summary'].items():
            print(f"{metric_name:4}: {metric_data['value']:8.4f} ({metric_data['status']})")
        
        # Print detailed metrics
        print("\n📋 Detailed Metrics:")
        print("-" * 40)
        
        for metric_name, metric_result in results['metrics_results'].items():
            if 'error' not in metric_result:
                print(f"\n{metric_name}:")
                for key, value in metric_result.items():
                    if isinstance(value, (int, float)):
                        print(f"  {key}: {value:.4f}")
                    else:
                        print(f"  {key}: {value}")


def test_simple_metrics():
    """Test simple metrics with sample data"""
    print("🚀 SIMPLE METRICS TEST SUITE")
    print("=" * 50)
    
    tester = SimpleMetricsTester()
    
    if not tester.setup():
        return False
    
    # Add test cases
    tester.add_test_case(
        "salam alaykum", 
        "سلام عليكم", 
        "Arabic", 
        "Arabic greeting"
    )
    
    tester.add_test_case(
        "habari yako", 
        "habari yako", 
        "Swahili", 
        "Swahili greeting"
    )
    
    tester.add_test_case(
        "hello world", 
        "hello world", 
        "English", 
        "English text"
    )
    
    tester.add_test_case(
        "merhaba", 
        "merhaba", 
        "Turkish", 
        "Turkish greeting"
    )
    
    # Run comprehensive evaluation
    results = tester.run_comprehensive_evaluation()
    
    if results:
        tester.print_detailed_results(results)
        return True
    else:
        print("❌ Simple metrics evaluation failed")
        return False


if __name__ == "__main__":
    success = test_simple_metrics()
    if success:
        print("\n🎉 Simple metrics test completed successfully!")
    else:
        print("\n❌ Simple metrics test failed!")
        sys.exit(1)
