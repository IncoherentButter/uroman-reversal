"""
Match Error Rate (MER) metric implementation.

MER measures the proportion of words that don't match exactly between
the original and reconstructed texts. It's a simpler metric than WER
that focuses on exact matches rather than edit operations.
"""

from typing import List, Dict, Any
from .base_metric import BaseMetric


class MatchErrorRate(BaseMetric):
    """
    Calculate Match Error Rate between original and reconstructed texts.
    
    MER = (Total Words - Matching Words) / Total Words
    where:
    - Total Words = number of words in reference
    - Matching Words = number of words that match exactly
    """
    
    def __init__(self):
        self.name = "Match Error Rate"
        self.description = "Proportion of words that don't match exactly between reference and hypothesis"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate MER for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing MER results and metadata
        """
        if not self.validate_inputs(reference_texts, hypothesis_texts):
            raise ValueError("Invalid inputs for MER calculation")
        
        total_mer = 0.0
        total_words = 0
        total_matches = 0
        individual_mer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            # Tokenize into words
            ref_words = self._tokenize_words(ref)
            hyp_words = self._tokenize_words(hyp)
            
            # Count exact matches
            matches = self._count_exact_matches(ref_words, hyp_words)
            
            # Calculate MER for this sample
            if len(ref_words) > 0:
                sample_mer = (len(ref_words) - matches) / len(ref_words)
                individual_mer.append(sample_mer)
                total_mer += (len(ref_words) - matches)
                total_words += len(ref_words)
                total_matches += matches
            else:
                individual_mer.append(0.0)
        
        # Calculate overall MER
        overall_mer = total_mer / total_words if total_words > 0 else 0.0
        
        return {
            'overall_mer': overall_mer,
            'individual_mer': individual_mer,
            'total_words': total_words,
            'total_matches': total_matches,
            'total_mismatches': total_mer,
            'match_rate': total_matches / total_words if total_words > 0 else 0.0,
            'sample_count': len(reference_texts),
            'metric_name': self.name,
            'description': self.description
        }
    
    def _tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words.
        
        Args:
            text: Input text
            
        Returns:
            List of words
        """
        # Basic word tokenization - can be overridden by language adapters
        return text.split()
    
    def _count_exact_matches(self, ref_words: List[str], hyp_words: List[str]) -> int:
        """
        Count the number of words that match exactly between reference and hypothesis.
        
        Args:
            ref_words: Reference word sequence
            hyp_words: Hypothesis word sequence
            
        Returns:
            Number of exact matches
        """
        # For exact matching, we need to align the sequences
        # This is a simple implementation - more sophisticated alignment
        # could be implemented for better accuracy
        
        matches = 0
        min_len = min(len(ref_words), len(hyp_words))
        
        # Count matches up to the shorter sequence length
        for i in range(min_len):
            if ref_words[i] == hyp_words[i]:
                matches += 1
        
        return matches
