"""
Base metric class for evaluation metrics.

This abstract class defines the interface that all evaluation metrics
must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseMetric(ABC):
    """
    Abstract base class for all evaluation metrics.
    
    This class defines the interface that all metrics must implement.
    It provides common functionality and ensures consistent behavior
    across different metric types.
    """
    
    def __init__(self):
        """Initialize the metric with name and description."""
        self.name = ""
        self.description = ""
    
    @abstractmethod
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate the metric value for the given text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters specific to the metric
            
        Returns:
            Dictionary containing metric results and metadata
        """
        pass
    
    def validate_inputs(self, 
                       reference_texts: List[str], 
                       hypothesis_texts: List[str]) -> bool:
        """
        Validate that inputs are suitable for metric calculation.
        
        Args:
            reference_texts: List of reference texts
            hypothesis_texts: List of hypothesis texts
            
        Returns:
            True if inputs are valid, False otherwise
        """
        if not reference_texts or not hypothesis_texts:
            return False
        
        if len(reference_texts) != len(hypothesis_texts):
            return False
        
        # Check that all texts are strings
        if not all(isinstance(text, str) for text in reference_texts + hypothesis_texts):
            return False
        
        return True
    
    def get_metric_info(self) -> Dict[str, str]:
        """
        Get basic information about the metric.
        
        Returns:
            Dictionary with metric name and description
        """
        return {
            'name': self.name,
            'description': self.description
        }
