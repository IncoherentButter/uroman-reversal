"""
Information preservation metrics implementation.

These metrics measure how well the reverse uroman process preserves
information from the original text, including character diversity,
vocabulary preservation, and semantic content retention.
"""

from typing import List, Dict, Any
from .base_metric import BaseMetric
import math


class InformationMetrics(BaseMetric):
    """
    Calculate information preservation metrics between original and reconstructed texts.
    
    This class provides multiple metrics to assess information retention:
    - Character diversity preservation
    - Vocabulary preservation  
    - Information entropy preservation
    - Semantic content retention
    """
    
    def __init__(self):
        self.name = "Information Metrics"
        self.description = "Multiple metrics for measuring information preservation"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate information preservation metrics for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing all information metrics and metadata
        """
        if not self.validate_inputs(reference_texts, hypothesis_texts):
            raise ValueError("Invalid inputs for information metrics calculation")
        
        results = {}
        
        # Calculate character diversity metrics
        char_diversity = self._calculate_character_diversity(reference_texts, hypothesis_texts)
        results.update(char_diversity)
        
        # Calculate vocabulary preservation metrics
        vocab_preservation = self._calculate_vocabulary_preservation(reference_texts, hypothesis_texts)
        results.update(vocab_preservation)
        
        # Calculate entropy preservation
        entropy_preservation = self._calculate_entropy_preservation(reference_texts, hypothesis_texts)
        results.update(entropy_preservation)
        
        # Add metadata
        results.update({
            'metric_name': self.name,
            'description': self.description,
            'sample_count': len(reference_texts)
        })
        
        return results
    
    def _calculate_character_diversity(self, 
                                     reference_texts: List[str], 
                                     hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate character diversity preservation metrics."""
        ref_chars = set()
        hyp_chars = set()
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_chars.update(ref)
            hyp_chars.update(hyp)
        
        # Calculate character diversity metrics
        ref_char_count = len(ref_chars)
        hyp_char_count = len(hyp_chars)
        preserved_chars = len(ref_chars.intersection(hyp_chars))
        lost_chars = len(ref_chars - hyp_chars)
        gained_chars = len(hyp_chars - ref_chars)
        
        char_preservation_rate = preserved_chars / ref_char_count if ref_char_count > 0 else 0.0
        char_loss_rate = lost_chars / ref_char_count if ref_char_count > 0 else 0.0
        
        return {
            'character_diversity': {
                'reference_char_count': ref_char_count,
                'hypothesis_char_count': hyp_char_count,
                'preserved_chars': preserved_chars,
                'lost_chars': lost_chars,
                'gained_chars': gained_chars,
                'preservation_rate': char_preservation_rate,
                'loss_rate': char_loss_rate
            }
        }
    
    def _calculate_vocabulary_preservation(self, 
                                         reference_texts: List[str], 
                                         hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate vocabulary preservation metrics."""
        ref_vocab = set()
        hyp_vocab = set()
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            ref_vocab.update(self._tokenize_words(ref))
            hyp_vocab.update(self._tokenize_words(hyp))
        
        # Calculate vocabulary metrics
        ref_vocab_size = len(ref_vocab)
        hyp_vocab_size = len(hyp_vocab)
        preserved_words = len(ref_vocab.intersection(hyp_vocab))
        lost_words = len(ref_vocab - hyp_vocab)
        gained_words = len(hyp_vocab - ref_vocab)
        
        vocab_preservation_rate = preserved_words / ref_vocab_size if ref_vocab_size > 0 else 0.0
        vocab_loss_rate = lost_words / ref_vocab_size if ref_vocab_size > 0 else 0.0
        
        return {
            'vocabulary_preservation': {
                'reference_vocab_size': ref_vocab_size,
                'hypothesis_vocab_size': hyp_vocab_size,
                'preserved_words': preserved_words,
                'lost_words': lost_words,
                'gained_words': gained_words,
                'preservation_rate': vocab_preservation_rate,
                'loss_rate': vocab_loss_rate
            }
        }
    
    def _calculate_entropy_preservation(self, 
                                      reference_texts: List[str], 
                                      hypothesis_texts: List[str]) -> Dict[str, Any]:
        """Calculate information entropy preservation metrics."""
        ref_entropy = self._calculate_text_entropy(' '.join(reference_texts))
        hyp_entropy = self._calculate_text_entropy(' '.join(hypothesis_texts))
        
        # Calculate entropy preservation
        entropy_difference = abs(ref_entropy - hyp_entropy)
        entropy_preservation_rate = 1.0 - (entropy_difference / ref_entropy) if ref_entropy > 0 else 0.0
        
        return {
            'entropy_preservation': {
                'reference_entropy': ref_entropy,
                'hypothesis_entropy': hyp_entropy,
                'entropy_difference': entropy_difference,
                'preservation_rate': entropy_preservation_rate
            }
        }
    
    def _calculate_text_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text."""
        if not text:
            return 0.0
        
        # Count character frequencies
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy
        text_length = len(text)
        entropy = 0.0
        
        for count in char_counts.values():
            probability = count / text_length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Tokenize text into words."""
        return text.split()
