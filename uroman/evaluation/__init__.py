"""
Evaluation framework for uroman reverse performance.

This module provides tools to measure how well reverse uroman performs
across different languages using various metrics like word error rate,
character error rate, and information preservation metrics.
"""

from .base_evaluator import BaseEvaluator
from .results_analyzer import ResultsAnalyzer
from .dataset_handlers.huggingface_handler import HuggingFaceDatasetHandler

__all__ = [
    'BaseEvaluator',
    'ResultsAnalyzer', 
    'HuggingFaceDatasetHandler',
]
