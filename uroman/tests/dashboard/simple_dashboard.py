#!/usr/bin/env python3

"""
Simple Metrics Dashboard for Reverse Uroman

This dashboard provides a visual way to view all 5 metrics without external dependencies:
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
import time
from datetime import datetime

# Add the uroman directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reverse_uroman import ReverseUroman, ReverseRomFormat
from tests.integration.test_simple_metrics import SimpleMetricsCalculator


class SimpleMetricsDashboard:
    """Simple dashboard for comprehensive metrics visualization"""
    
    def __init__(self):
        """Initialize the simple metrics dashboard"""
        self.reverse_uroman = None
        self.metrics_calculator = SimpleMetricsCalculator()
        self.test_data = []
        self.results_history = []
        
    def setup(self):
        """Set up the reverse uroman and metrics calculator"""
        try:
            self.reverse_uroman = ReverseUroman()
            print("✅ Simple Metrics Dashboard initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize dashboard: {e}")
            return False
    
    def add_test_data(self, input_text: str, expected_output: str, 
                     target_script: str, description: str = ""):
        """Add test data to the dashboard"""
        self.test_data.append({
            'input': input_text,
            'expected': expected_output,
            'target_script': target_script,
            'description': description,
            'timestamp': datetime.now().isoformat()
        })
    
    def load_sample_data(self):
        """Load sample test data for demonstration"""
        sample_data = [
            ("salam alaykum", "سلام عليكم", "Arabic", "Arabic greeting"),
            ("habari yako", "habari yako", "Swahili", "Swahili greeting"),
            ("hello world", "hello world", "English", "English text"),
            ("merhaba", "merhaba", "Turkish", "Turkish greeting"),
            ("bonjour", "bonjour", "French", "French greeting"),
            ("hola", "hola", "Spanish", "Spanish greeting"),
            ("namaste", "नमस्ते", "Hindi", "Hindi greeting"),
            ("konnichiwa", "こんにちは", "Japanese", "Japanese greeting"),
        ]
        
        for input_text, expected, script, desc in sample_data:
            self.add_test_data(input_text, expected, script, desc)
        
        print(f"📊 Loaded {len(sample_data)} sample test cases")
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run comprehensive evaluation with all metrics"""
        if not self.test_data:
            print("❌ No test data available")
            return {}
        
        print("🔍 Running Comprehensive Evaluation")
        print("=" * 50)
        
        # Prepare data for metrics
        reference_texts = []
        hypothesis_texts = []
        test_results = []
        
        for i, test_case in enumerate(self.test_data, 1):
            print(f"Processing test {i}/{len(self.test_data)}: {test_case['description']}")
            
            try:
                # Perform reverse romanization
                result = self.reverse_uroman.reverse_romanize_string(
                    test_case['input'], 
                    test_case['target_script']
                )
                
                # Store for metrics calculation
                reference_texts.append(test_case['expected'])
                hypothesis_texts.append(result)
                
                test_results.append({
                    'test_id': i,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'output': result,
                    'target_script': test_case['target_script'],
                    'description': test_case['description'],
                    'success': True
                })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                test_results.append({
                    'test_id': i,
                    'input': test_case['input'],
                    'expected': test_case['expected'],
                    'output': None,
                    'target_script': test_case['target_script'],
                    'description': test_case['description'],
                    'success': False,
                    'error': str(e)
                })
        
        if not reference_texts:
            print("❌ No successful test cases for metrics calculation")
            return {}
        
        print(f"\n📊 Calculating all 5 metrics on {len(reference_texts)} successful test cases")
        
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
        
        # Store results in history
        evaluation_result = {
            'timestamp': datetime.now().isoformat(),
            'test_results': test_results,
            'metrics_results': metrics_results,
            'summary': self._generate_summary(metrics_results, test_results)
        }
        
        self.results_history.append(evaluation_result)
        
        return evaluation_result
    
    def _generate_summary(self, metrics_results: Dict[str, Any], test_results: List[Dict]) -> Dict[str, Any]:
        """Generate a comprehensive summary of all metrics"""
        successful_tests = len([r for r in test_results if r['success']])
        total_tests = len(test_results)
        
        summary = {
            'evaluation_info': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0.0,
                'timestamp': datetime.now().isoformat()
            },
            'metrics_overview': {},
            'performance_analysis': {}
        }
        
        # Process each metric
        for metric_name, result in metrics_results.items():
            if 'error' not in result:
                overall_key = f'overall_{metric_name.lower()}'
                if overall_key in result:
                    value = result[overall_key]
                    summary['metrics_overview'][metric_name] = {
                        'value': value,
                        'status': '✅ Calculated',
                        'interpretation': self._interpret_metric(metric_name, value)
                    }
                else:
                    summary['metrics_overview'][metric_name] = {
                        'value': 'N/A',
                        'status': '⚠️ No overall value',
                        'interpretation': 'Unable to calculate'
                    }
            else:
                summary['metrics_overview'][metric_name] = {
                    'value': 'N/A',
                    'status': f'❌ Error: {result["error"]}',
                    'interpretation': 'Calculation failed'
                }
        
        # Performance analysis
        summary['performance_analysis'] = self._analyze_performance(metrics_results)
        
        return summary
    
    def _interpret_metric(self, metric_name: str, value: float) -> str:
        """Interpret metric values for user understanding"""
        interpretations = {
            'WER': f"Word Error Rate: {value:.1%} of words have errors",
            'CER': f"Character Error Rate: {value:.1%} of characters have errors", 
            'MER': f"Match Error Rate: {value:.1%} of words don't match exactly",
            'WIL': f"Word Information Lost: {value:.1%} of word-level information lost",
            'WIP': f"Word Information Preserved: {value:.1%} of word-level information preserved"
        }
        return interpretations.get(metric_name, f"Value: {value:.4f}")
    
    def _analyze_performance(self, metrics_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze overall performance based on metrics"""
        analysis = {
            'overall_quality': 'Unknown',
            'recommendations': [],
            'strengths': [],
            'weaknesses': []
        }
        
        # Analyze each metric
        if 'WER' in metrics_results and 'error' not in metrics_results['WER']:
            wer = metrics_results['WER'].get('overall_wer', 1.0)
            if wer < 0.1:
                analysis['strengths'].append("Excellent word accuracy")
            elif wer < 0.3:
                analysis['strengths'].append("Good word accuracy")
            else:
                analysis['weaknesses'].append("Poor word accuracy")
        
        if 'CER' in metrics_results and 'error' not in metrics_results['CER']:
            cer = metrics_results['CER'].get('overall_cer', 1.0)
            if cer < 0.05:
                analysis['strengths'].append("Excellent character accuracy")
            elif cer < 0.2:
                analysis['strengths'].append("Good character accuracy")
            else:
                analysis['weaknesses'].append("Poor character accuracy")
        
        if 'WIP' in metrics_results and 'error' not in metrics_results['WIP']:
            wip = metrics_results['WIP'].get('overall_wip', 0.0)
            if wip > 0.8:
                analysis['strengths'].append("Excellent information preservation")
            elif wip > 0.6:
                analysis['strengths'].append("Good information preservation")
            else:
                analysis['weaknesses'].append("Poor information preservation")
        
        # Overall quality assessment
        if len(analysis['strengths']) >= 2 and len(analysis['weaknesses']) == 0:
            analysis['overall_quality'] = 'Excellent'
        elif len(analysis['strengths']) > len(analysis['weaknesses']):
            analysis['overall_quality'] = 'Good'
        elif len(analysis['weaknesses']) > len(analysis['strengths']):
            analysis['overall_quality'] = 'Needs Improvement'
        else:
            analysis['overall_quality'] = 'Mixed'
        
        # Generate recommendations
        if 'Poor word accuracy' in analysis['weaknesses']:
            analysis['recommendations'].append("Improve word-level romanization accuracy")
        if 'Poor character accuracy' in analysis['weaknesses']:
            analysis['recommendations'].append("Improve character-level romanization accuracy")
        if 'Poor information preservation' in analysis['weaknesses']:
            analysis['recommendations'].append("Improve information preservation during romanization")
        
        return analysis
    
    def display_dashboard(self, results: Dict[str, Any]):
        """Display the comprehensive metrics dashboard"""
        if not results:
            print("❌ No results to display")
            return
        
        print("\n" + "=" * 80)
        print("📊 SIMPLE METRICS DASHBOARD")
        print("=" * 80)
        
        # Header with evaluation info
        eval_info = results['summary']['evaluation_info']
        print(f"\n📅 Evaluation Date: {eval_info['timestamp']}")
        print(f"🧪 Tests: {eval_info['successful_tests']}/{eval_info['total_tests']} successful ({eval_info['success_rate']:.1%})")
        
        # Metrics overview
        print(f"\n📈 METRICS OVERVIEW")
        print("-" * 50)
        for metric_name, metric_data in results['summary']['metrics_overview'].items():
            print(f"{metric_name:4}: {str(metric_data['value']):>8} | {metric_data['status']}")
            print(f"      {metric_data['interpretation']}")
            print()
        
        # Performance analysis
        perf = results['summary']['performance_analysis']
        print(f"🎯 PERFORMANCE ANALYSIS")
        print("-" * 50)
        print(f"Overall Quality: {perf['overall_quality']}")
        
        if perf['strengths']:
            print(f"\n✅ Strengths:")
            for strength in perf['strengths']:
                print(f"   • {strength}")
        
        if perf['weaknesses']:
            print(f"\n⚠️  Areas for Improvement:")
            for weakness in perf['weaknesses']:
                print(f"   • {weakness}")
        
        if perf['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in perf['recommendations']:
                print(f"   • {rec}")
        
        # Test results details
        print(f"\n📋 DETAILED TEST RESULTS")
        print("-" * 50)
        for test_result in results['test_results']:
            status = "✅" if test_result['success'] else "❌"
            print(f"{status} Test {test_result['test_id']}: {test_result['description']}")
            print(f"   Input:    '{test_result['input']}'")
            print(f"   Expected: '{test_result['expected']}'")
            if test_result['success']:
                print(f"   Output:   '{test_result['output']}'")
            else:
                print(f"   Error:    {test_result.get('error', 'Unknown error')}")
            print()
    
    def export_results(self, results: Dict[str, Any], filename: str = None):
        """Export results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simple_metrics_dashboard_results_{timestamp}.json"
        
        filepath = Path(__file__).parent / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"📁 Results exported to: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Failed to export results: {e}")
            return None
    
    def run_interactive_dashboard(self):
        """Run the interactive dashboard"""
        print("🚀 Starting Simple Metrics Dashboard")
        print("=" * 50)
        
        if not self.setup():
            return False
        
        # Load sample data
        self.load_sample_data()
        
        # Run evaluation
        results = self.run_evaluation()
        
        if results:
            # Display dashboard
            self.display_dashboard(results)
            
            # Export results
            export_path = self.export_results(results)
            
            print(f"\n🎉 Dashboard completed successfully!")
            if export_path:
                print(f"📁 Results saved to: {export_path}")
            
            return True
        else:
            print("❌ Dashboard failed to generate results")
            return False


def main():
    """Main function to run the simple metrics dashboard"""
    dashboard = SimpleMetricsDashboard()
    success = dashboard.run_interactive_dashboard()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
