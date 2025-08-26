"""
Results analyzer for evaluation framework.

This module provides functionality to aggregate, analyze, and visualize
evaluation results from different metrics and languages.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from .base_evaluator import EvaluationResult


class ResultsAnalyzer:
    """
    Analyzer for evaluation results.
    
    This class provides methods to aggregate results from different
    evaluation runs, generate statistics, and create visualizations.
    """
    
    def __init__(self):
        """Initialize the results analyzer."""
        self.results: List[EvaluationResult] = []
        self.logger = logging.getLogger(__name__)
    
    def add_results(self, results: List[EvaluationResult]) -> None:
        """
        Add evaluation results to the analyzer.
        
        Args:
            results: List of evaluation results to add
        """
        self.results.extend(results)
        self.logger.info(f"Added {len(results)} results to analyzer")
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Generate summary statistics for all results.
        
        Returns:
            Dictionary containing summary statistics
        """
        if not self.results:
            return {'status': 'No results available'}
        
        summary = {
            'total_evaluations': len(self.results),
            'languages': list(set(r.language for r in self.results)),
            'metrics': list(set(r.metric_name for r in self.results)),
            'overall_summary': {},
            'by_language': {},
            'by_metric': {}
        }
        
        # Calculate overall summary
        for metric_name in summary['metrics']:
            metric_results = [r for r in self.results if r.metric_name == metric_name]
            if metric_results:
                values = [r.value for r in metric_results]
                summary['overall_summary'][metric_name] = {
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values)
                }
        
        # Calculate by language
        for language in summary['languages']:
            lang_results = [r for r in self.results if r.language == language]
            summary['by_language'][language] = {
                'total_samples': sum(r.sample_size for r in lang_results),
                'metrics': {}
            }
            
            for metric_name in summary['metrics']:
                metric_results = [r for r in lang_results if r.metric_name == metric_name]
                if metric_results:
                    values = [r.value for r in metric_results]
                    summary['by_language'][language]['metrics'][metric_name] = {
                        'mean': sum(values) / len(values),
                        'min': min(values),
                        'max': max(values),
                        'count': len(values)
                    }
        
        # Calculate by metric
        for metric_name in summary['metrics']:
            metric_results = [r for r in self.results if r.metric_name == metric_name]
            summary['by_metric'][metric_name] = {
                'total_samples': sum(r.sample_size for r in metric_results),
                'languages': list(set(r.language for r in metric_results)),
                'overall_mean': sum(r.value for r in metric_results) / len(metric_results)
            }
        
        return summary
    
    def export_results(self, 
                      output_path: str, 
                      format: str = 'json') -> None:
        """
        Export results to a file.
        
        Args:
            output_path: Path to save the results
            format: Output format ('json' or 'csv')
        """
        if not self.results:
            self.logger.warning("No results to export")
            return
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if format.lower() == 'json':
                self._export_json(output_path)
            elif format.lower() == 'csv':
                self._export_csv(output_path)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.logger.info(f"Results exported to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            raise
    
    def _export_json(self, output_path: Path) -> None:
        """Export results to JSON format."""
        # Convert results to serializable format
        serializable_results = []
        for result in self.results:
            serializable_results.append({
                'metric_name': result.metric_name,
                'value': result.value,
                'metadata': result.metadata,
                'language': result.language,
                'sample_size': result.sample_size
            })
        
        # Add summary statistics
        export_data = {
            'results': serializable_results,
            'summary': self.get_summary_statistics()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    def _export_csv(self, output_path: Path) -> None:
        """Export results to CSV format."""
        # Convert results to DataFrame
        data = []
        for result in self.results:
            data.append({
                'metric_name': result.metric_name,
                'value': result.value,
                'language': result.language,
                'sample_size': result.sample_size,
                'metadata': json.dumps(result.metadata)
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
    
    def create_visualizations(self, 
                             output_dir: str,
                             include_plots: bool = True) -> None:
        """
        Create visualizations of the results.
        
        Args:
            output_dir: Directory to save visualizations
            include_plots: Whether to generate matplotlib plots
        """
        if not self.results:
            self.logger.warning("No results to visualize")
            return
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if include_plots:
                self._create_plots(output_dir)
            
            # Create summary report
            self._create_summary_report(output_dir)
            
            self.logger.info(f"Visualizations created in: {output_dir}")
            
        except Exception as e:
            self.logger.error(f"Failed to create visualizations: {e}")
            raise
    
    def _create_plots(self, output_dir: Path) -> None:
        """Create matplotlib plots of the results."""
        # Set up plotting style
        plt.style.use('default')
        
        # Create metric comparison plot
        self._plot_metric_comparison(output_dir)
        
        # Create language comparison plot
        self._plot_language_comparison(output_dir)
        
        # Create sample size distribution plot
        self._plot_sample_distribution(output_dir)
    
    def _plot_metric_comparison(self, output_dir: Path) -> None:
        """Create plot comparing different metrics."""
        summary = self.get_summary_statistics()
        
        if 'overall_summary' not in summary:
            return
        
        metrics = list(summary['overall_summary'].keys())
        means = [summary['overall_summary'][m]['mean'] for m in metrics]
        
        plt.figure(figsize=(10, 6))
        plt.bar(metrics, means)
        plt.title('Overall Metric Performance')
        plt.ylabel('Mean Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(output_dir / 'metric_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_language_comparison(self, output_dir: Path) -> None:
        """Create plot comparing different languages."""
        summary = self.get_summary_statistics()
        
        if 'by_language' not in summary:
            return
        
        # Get the first metric for comparison
        if not summary['metrics']:
            return
        
        metric_name = summary['metrics'][0]
        languages = []
        values = []
        
        for lang, data in summary['by_language'].items():
            if metric_name in data['metrics']:
                languages.append(lang)
                values.append(data['metrics'][metric_name]['mean'])
        
        if not languages:
            return
        
        plt.figure(figsize=(10, 6))
        plt.bar(languages, values)
        plt.title(f'{metric_name} by Language')
        plt.ylabel('Mean Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(output_dir / 'language_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _plot_sample_distribution(self, output_dir: Path) -> None:
        """Create plot showing sample size distribution."""
        sample_sizes = [r.sample_size for r in self.results]
        
        plt.figure(figsize=(10, 6))
        plt.hist(sample_sizes, bins=20, edgecolor='black')
        plt.title('Sample Size Distribution')
        plt.xlabel('Sample Size')
        plt.ylabel('Frequency')
        plt.tight_layout()
        
        plt.savefig(output_dir / 'sample_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def _create_summary_report(self, output_dir: Path) -> None:
        """Create a text summary report."""
        summary = self.get_summary_statistics()
        
        report_path = output_dir / 'summary_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Uroman Reverse Evaluation Results Summary\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total Evaluations: {summary.get('total_evaluations', 0)}\n")
            f.write(f"Languages Evaluated: {', '.join(summary.get('languages', []))}\n")
            f.write(f"Metrics Used: {', '.join(summary.get('metrics', []))}\n\n")
            
            f.write("Overall Summary:\n")
            f.write("-" * 20 + "\n")
            for metric, data in summary.get('overall_summary', {}).items():
                f.write(f"{metric}:\n")
                f.write(f"  Mean: {data['mean']:.4f}\n")
                f.write(f"  Range: {data['min']:.4f} - {data['max']:.4f}\n")
                f.write(f"  Count: {data['count']}\n\n")
            
            f.write("By Language:\n")
            f.write("-" * 20 + "\n")
            for lang, data in summary.get('by_language', {}).items():
                f.write(f"{lang}:\n")
                f.write(f"  Total Samples: {data['total_samples']}\n")
                for metric, metric_data in data.get('metrics', {}).items():
                    f.write(f"  {metric}: {metric_data['mean']:.4f}\n")
                f.write("\n")
    
    def get_best_performing_language(self, metric_name: str) -> Optional[str]:
        """
        Get the language with the best performance for a specific metric.
        
        Args:
            metric_name: Name of the metric to check
            
        Returns:
            Language code with best performance, or None if no results
        """
        metric_results = [r for r in self.results if r.metric_name == metric_name]
        
        if not metric_results:
            return None
        
        # Find language with best (lowest) value for error rate metrics
        best_result = min(metric_results, key=lambda x: x.value)
        return best_result.language
    
    def get_worst_performing_language(self, metric_name: str) -> Optional[str]:
        """
        Get the language with the worst performance for a specific metric.
        
        Args:
            metric_name: Name of the metric to check
            
        Returns:
            Language code with worst performance, or None if no results
        """
        metric_results = [r for r in self.results if r.metric_name == metric_name]
        
        if not metric_results:
            return None
        
        # Find language with worst (highest) value for error rate metrics
        worst_result = max(metric_results, key=lambda x: x.value)
        return worst_result.language
