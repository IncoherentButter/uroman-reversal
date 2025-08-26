"""
Base evaluator class for uroman reverse performance evaluation.

This abstract class defines the interface that all language-specific
evaluators must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Container for evaluation results."""
    metric_name: str
    value: float
    metadata: Dict[str, Any]
    language: str
    sample_size: int


class BaseEvaluator(ABC):
    """
    Abstract base class for evaluating reverse uroman performance.
    
    This class defines the interface that all language-specific evaluators
    must implement. It provides common functionality for running evaluations
    and collecting results.
    """
    
    def __init__(self, language: str):
        """
        Initialize the evaluator.
        
        Args:
            language: The language code (e.g., 'ar', 'zh', 'ja')
        """
        self.language = language
        self.results: List[EvaluationResult] = []
    
    @abstractmethod
    def evaluate_word_error_rate(self, 
                               original_texts: List[str], 
                               reconstructed_texts: List[str]) -> EvaluationResult:
        """
        Calculate word error rate between original and reconstructed texts.
        
        Args:
            original_texts: List of original text samples
            reconstructed_texts: List of reconstructed text samples
            
        Returns:
            EvaluationResult with WER metric
        """
        pass
    
    @abstractmethod
    def evaluate_character_error_rate(self, 
                                   original_texts: List[str], 
                                   reconstructed_texts: List[str]) -> EvaluationResult:
        """
        Calculate character error rate between original and reconstructed texts.
        
        Args:
            original_texts: List of original text samples
            reconstructed_texts: List of reconstructed text samples
            
        Returns:
            EvaluationResult with CER metric
        """
        pass
    
    @abstractmethod
    def evaluate_match_error_rate(self, 
                               original_texts: List[str], 
                               reconstructed_texts: List[str]) -> EvaluationResult:
        """
        Calculate match error rate between original and reconstructed texts.
        
        Args:
            original_texts: List of original text samples
            reconstructed_texts: List of reconstructed text samples
            
        Returns:
            EvaluationResult with MER metric
        """
        pass
    
    @abstractmethod
    def evaluate_information_preservation(self, 
                                       original_texts: List[str], 
                                       reconstructed_texts: List[str]) -> EvaluationResult:
        """
        Calculate information preservation metrics.
        
        Args:
            original_texts: List of original text samples
            reconstructed_texts: List of reconstructed text samples
            
        Returns:
            EvaluationResult with information preservation metrics
        """
        pass
    
    def run_full_evaluation(self, 
                          original_texts: List[str], 
                          reconstructed_texts: List[str]) -> List[EvaluationResult]:
        """
        Run all evaluation metrics on the given texts.
        
        Args:
            original_texts: List of original text samples
            reconstructed_texts: List of reconstructed text samples
            
        Returns:
            List of all evaluation results
        """
        results = []
        
        # Run all metrics
        results.append(self.evaluate_word_error_rate(original_texts, reconstructed_texts))
        results.append(self.evaluate_character_error_rate(original_texts, reconstructed_texts))
        results.append(self.evaluate_match_error_rate(original_texts, reconstructed_texts))
        results.append(self.evaluate_information_preservation(original_texts, reconstructed_texts))
        
        # Store results
        self.results.extend(results)
        
        return results
    
    def get_results_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all evaluation results.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.results:
            return {}
        
        summary = {
            'language': self.language,
            'total_samples': sum(r.sample_size for r in self.results),
            'metrics': {}
        }
        
        for result in self.results:
            summary['metrics'][result.metric_name] = {
                'value': result.value,
                'metadata': result.metadata
            }
        
        return summary
