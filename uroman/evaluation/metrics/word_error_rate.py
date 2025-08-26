"""
Word Error Rate (WER) metric implementation.

WER measures the minimum number of word-level operations (insertions,
deletions, substitutions) needed to transform the reconstructed text
into the original text, divided by the total number of words in the original.
"""

from typing import List, Dict, Any
from .base_metric import BaseMetric


class WordErrorRate(BaseMetric):
    """
    Calculate Word Error Rate between original and reconstructed texts.
    
    WER = (S + D + I) / N
    where:
    - S = substitutions
    - D = deletions  
    - I = insertions
    - N = total words in reference
    """
    
    def __init__(self):
        self.name = "Word Error Rate"
        self.description = "Minimum word-level edit distance normalized by reference length"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate WER for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing WER results and metadata
        """
        if len(reference_texts) != len(hypothesis_texts):
            raise ValueError("Reference and hypothesis lists must have same length")
        
        total_wer = 0.0
        total_words = 0
        individual_wer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            # Tokenize into words
            ref_words = self._tokenize_words(ref)
            hyp_words = self._tokenize_words(hyp)
            
            # Calculate edit distance
            distance = self._levenshtein_distance(ref_words, hyp_words)
            
            # Calculate WER for this sample
            if len(ref_words) > 0:
                sample_wer = distance / len(ref_words)
                individual_wer.append(sample_wer)
                total_wer += distance
                total_words += len(ref_words)
            else:
                individual_wer.append(0.0)
        
        # Calculate overall WER
        overall_wer = total_wer / total_words if total_words > 0 else 0.0
        
        return {
            'overall_wer': overall_wer,
            'individual_wer': individual_wer,
            'total_words': total_words,
            'total_edits': total_wer,
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
    
    def _levenshtein_distance(self, ref_words: List[str], hyp_words: List[str]) -> int:
        """
        Calculate minimum edit distance between word sequences.
        
        Args:
            ref_words: Reference word sequence
            hyp_words: Hypothesis word sequence
            
        Returns:
            Minimum number of edits needed
        """
        # Dynamic programming implementation of Levenshtein distance
        m, n = len(ref_words), len(hyp_words)
        
        # Create matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Initialize first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Fill matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if ref_words[i-1] == hyp_words[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + 1,    # deletion
                        dp[i][j-1] + 1,    # insertion
                        dp[i-1][j-1] + 1   # substitution
                    )
        
        return dp[m][n]
