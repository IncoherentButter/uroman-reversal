#!/usr/bin/env python3

"""
Comprehensive Metrics Test Suite for Reverse Uroman

This script tests all 5 key metrics:
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

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat
from evaluation.metrics import (
    WordErrorRate, 
    CharacterErrorRate, 
    MatchErrorRate,
    WordInformationLost,
    WordInformationPreserved
)


class ComprehensiveMetricsTester:
    """Test class for comprehensive metrics evaluation"""
    
    def __init__(self):
        """Initialize the comprehensive metrics tester"""
        self.reverse_uroman = None
        self.metrics = {}
        self.test_cases = []
        
    def setup(self):
        """Set up the reverse uroman and all metrics"""
        try:
            self.reverse_uroman = ReverseUroman()
            
            # Initialize all 5 metrics
            self.metrics = {
                'wer': WordErrorRate(),
                'cer': CharacterErrorRate(),
                'mer': MatchErrorRate(),
                'wil': WordInformationLost(),
                'wip': WordInformationPreserved()
            }
            
            print("✅ Successfully initialized reverse uroman and all 5 metrics")
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
        
        print("🔍 Running Comprehensive Metrics Evaluation")
        print("=" * 60)
        
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
                result = self.reverse_uroman.reverse_romanize(
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
        print("-" * 60)
        
        # Calculate all metrics
        metrics_results = {}
        
        for metric_name, metric in self.metrics.items():
            try:
                print(f"   Calculating {metric.name}...")
                result = metric.calculate(reference_texts, hypothesis_texts)
                metrics_results[metric_name] = result
                print(f"   ✅ {metric.name}: {result.get(f'overall_{metric_name}', 'N/A')}")
            except Exception as e:
                print(f"   ❌ Error calculating {metric_name}: {e}")
                metrics_results[metric_name] = {'error': str(e)}
        
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
                overall_key = f'overall_{metric_name}'
                if overall_key in result:
                    summary['metrics_summary'][metric_name.upper()] = {
                        'value': result[overall_key],
                        'status': '✅ Calculated'
                    }
                else:
                    summary['metrics_summary'][metric_name.upper()] = {
                        'value': 'N/A',
                        'status': '⚠️ No overall value'
                    }
            else:
                summary['metrics_summary'][metric_name.upper()] = {
                    'value': 'N/A',
                    'status': f'❌ Error: {result["error"]}'
                }
        
        return summary
    
    def print_detailed_results(self, results: Dict[str, Any]):
        """Print detailed results for all metrics"""
        if not results:
            print("❌ No results to display")
            return
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE METRICS RESULTS")
        print("=" * 80)
        
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
            print(f"{metric_name:4}: {metric_data['value']:8} ({metric_data['status']})")
        
        # Print detailed metrics
        print("\n📋 Detailed Metrics:")
        print("-" * 40)
        
        for metric_name, metric_result in results['metrics_results'].items():
            if 'error' not in metric_result:
                print(f"\n{metric_name.upper()}:")
                for key, value in metric_result.items():
                    if key not in ['metric_name', 'description']:
                        if isinstance(value, (int, float)):
                            print(f"  {key}: {value:.4f}")
                        else:
                            print(f"  {key}: {value}")


def test_comprehensive_metrics():
    """Test comprehensive metrics with sample data"""
    print("🚀 COMPREHENSIVE METRICS TEST SUITE")
    print("=" * 60)
    
    tester = ComprehensiveMetricsTester()
    
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
        print("❌ Comprehensive metrics evaluation failed")
        return False


if __name__ == "__main__":
    success = test_comprehensive_metrics()
    if success:
        print("\n🎉 Comprehensive metrics test completed successfully!")
    else:
        print("\n❌ Comprehensive metrics test failed!")
        sys.exit(1)
