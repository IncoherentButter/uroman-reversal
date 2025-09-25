"""
Word Information Lost (WIL) and Word Information Preserved (WIP) metrics implementation.

These metrics measure how well the reverse uroman process preserves information
at the word level, focusing on semantic content and information density.
"""

from typing import List, Dict, Any
from .base_metric import BaseMetric
import math
from collections import Counter


class WordInformationLost(BaseMetric):
    """
    Calculate Word Information Lost (WIL) between original and reconstructed texts.
    
    WIL measures the proportion of information content lost during reverse romanization
    at the word level. It considers both lexical and semantic information.
    """
    
    def __init__(self):
        self.name = "Word Information Lost"
        self.description = "Measures information content lost at word level during reverse romanization"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate WIL for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing WIL results and metadata
        """
        if not self.validate_inputs(reference_texts, hypothesis_texts):
            raise ValueError("Invalid inputs for WIL calculation")
        
        total_wil = 0.0
        total_words = 0
        individual_wil = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = self._tokenize_words(ref)
            hyp_words = self._tokenize_words(hyp)
            
            if len(ref_words) > 0:
                # Calculate information content for reference words
                ref_info_content = self._calculate_word_information_content(ref_words)
                
                # Calculate information content for hypothesis words
                hyp_info_content = self._calculate_word_information_content(hyp_words)
                
                # Calculate WIL for this sample
                sample_wil = (ref_info_content - hyp_info_content) / ref_info_content if ref_info_content > 0 else 0.0
                individual_wil.append(max(0.0, sample_wil))  # WIL cannot be negative
                total_wil += sample_wil * len(ref_words)
                total_words += len(ref_words)
            else:
                individual_wil.append(0.0)
        
        # Calculate overall WIL
        overall_wil = total_wil / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wil': overall_wil,
            'individual_wil': individual_wil,
            'total_words': total_words,
            'total_information_lost': total_wil,
            'metric_name': self.name,
            'description': self.description
        }
    
    def _calculate_word_information_content(self, words: List[str]) -> float:
        """Calculate information content of a list of words."""
        if not words:
            return 0.0
        
        # Calculate word frequency distribution
        word_counts = Counter(words)
        total_words = len(words)
        
        # Calculate information entropy
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Information content is proportional to entropy and word count
        return entropy * total_words
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()


class WordInformationPreserved(BaseMetric):
    """
    Calculate Word Information Preserved (WIP) between original and reconstructed texts.
    
    WIP measures the proportion of information content preserved during reverse romanization
    at the word level. It's the complement of WIL.
    """
    
    def __init__(self):
        self.name = "Word Information Preserved"
        self.description = "Measures information content preserved at word level during reverse romanization"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate WIP for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing WIP results and metadata
        """
        if not self.validate_inputs(reference_texts, hypothesis_texts):
            raise ValueError("Invalid inputs for WIP calculation")
        
        total_wip = 0.0
        total_words = 0
        individual_wip = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_words = self._tokenize_words(ref)
            hyp_words = self._tokenize_words(hyp)
            
            if len(ref_words) > 0:
                # Calculate information content for reference words
                ref_info_content = self._calculate_word_information_content(ref_words)
                
                # Calculate information content for hypothesis words
                hyp_info_content = self._calculate_word_information_content(hyp_words)
                
                # Calculate WIP for this sample (preserved = min(hyp/ref, 1.0))
                sample_wip = min(hyp_info_content / ref_info_content, 1.0) if ref_info_content > 0 else 0.0
                individual_wip.append(sample_wip)
                total_wip += sample_wip * len(ref_words)
                total_words += len(ref_words)
            else:
                individual_wip.append(0.0)
        
        # Calculate overall WIP
        overall_wip = total_wip / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wip': overall_wip,
            'individual_wip': individual_wip,
            'total_words': total_words,
            'total_information_preserved': total_wip,
            'metric_name': self.name,
            'description': self.description
        }
    
    def _calculate_word_information_content(self, words: List[str]) -> float:
        """Calculate information content of a list of words."""
        if not words:
            return 0.0
        
        # Calculate word frequency distribution
        word_counts = Counter(words)
        total_words = len(words)
        
        # Calculate information entropy
        entropy = 0.0
        for count in word_counts.values():
            probability = count / total_words
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        # Information content is proportional to entropy and word count
        return entropy * total_words
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
