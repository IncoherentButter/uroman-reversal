"""
Character Error Rate (CER) metric implementation.

CER measures the minimum number of character-level operations (insertions,
deletions, substitutions) needed to transform the reconstructed text
into the original text, divided by the total number of characters in the original.
"""

from typing import List, Dict, Any
from .base_metric import BaseMetric


class CharacterErrorRate(BaseMetric):
    """
    Calculate Character Error Rate between original and reconstructed texts.
    
    CER = (S + D + I) / N
    where:
    - S = character substitutions
    - D = character deletions  
    - I = character insertions
    - N = total characters in reference
    """
    
    def __init__(self):
        self.name = "Character Error Rate"
        self.description = "Minimum character-level edit distance normalized by reference length"
    
    def calculate(self, 
                 reference_texts: List[str], 
                 hypothesis_texts: List[str],
                 **kwargs) -> Dict[str, Any]:
        """
        Calculate CER for a batch of text pairs.
        
        Args:
            reference_texts: List of reference (original) texts
            hypothesis_texts: List of hypothesis (reconstructed) texts
            **kwargs: Additional parameters
            
        Returns:
            Dictionary containing CER results and metadata
        """
        if not self.validate_inputs(reference_texts, hypothesis_texts):
            raise ValueError("Invalid inputs for CER calculation")
        
        total_cer = 0.0
        total_chars = 0
        individual_cer = []
        
        for ref, hyp in zip(reference_texts, hypothesis_texts):
            # Calculate edit distance at character level
            distance = self._levenshtein_distance(ref, hyp)
            
            # Calculate CER for this sample
            if len(ref) > 0:
                sample_cer = distance / len(ref)
                individual_cer.append(sample_cer)
                total_cer += distance
                total_chars += len(ref)
            else:
                individual_cer.append(0.0)
        
        # Calculate overall CER
        overall_cer = total_cer / total_chars if total_chars > 0 else 0.0
        
        return {
            'overall_cer': overall_cer,
            'individual_cer': individual_cer,
            'total_chars': total_chars,
            'total_edits': total_cer,
            'sample_count': len(reference_texts),
            'metric_name': self.name,
            'description': self.description
        }
    
    def _levenshtein_distance(self, ref: str, hyp: str) -> int:
        """
        Calculate minimum edit distance between character sequences.
        
        Args:
            ref: Reference character sequence
            hyp: Hypothesis character sequence
            
        Returns:
            Minimum number of edits needed
        """
        # Dynamic programming implementation of Levenshtein distance
        m, n = len(ref), len(hyp)
        
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
                if ref[i-1] == hyp[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = min(
                        dp[i-1][j] + 1,    # deletion
                        dp[i][j-1] + 1,    # insertion
                        dp[i-1][j-1] + 1   # substitution
                    )
        
        return dp[m][n]
