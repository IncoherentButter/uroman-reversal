"""
Arabic language adapter for evaluation framework.

This adapter handles Arabic-specific characteristics including:
- Right-to-left text direction
- Diacritical marks (harakat)
- Arabic script ligatures
- Arabic-specific normalization
"""

import re
from typing import List, Dict, Any
from .base_adapter import BaseLanguageAdapter


class ArabicAdapter(BaseLanguageAdapter):
    """
    Language adapter for Arabic text evaluation.
    
    Handles Arabic-specific preprocessing, tokenization, and normalization
    to ensure accurate evaluation of reverse uroman performance on Arabic text.
    """
    
    def __init__(self):
        """Initialize the Arabic language adapter."""
        super().__init__('ar')
        
        # Arabic-specific Unicode ranges
        self.arabic_chars = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        self.diacritics = re.compile(r'[\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED]')
        
        # Common Arabic ligatures
        self.ligatures = {
            'لا': 'ل + ا',
            'لآ': 'ل + آ',
            'لأ': 'ل + أ',
            'لإ': 'ل + إ',
            'لئ': 'ل + ئ',
            'لؤ': 'ل + ؤ',
            'لء': 'ل + ء'
        }
    
    def preprocess_for_evaluation(self, text: str) -> str:
        """
        Preprocess Arabic text for evaluation.
        
        This method handles Arabic-specific preprocessing to ensure
        fair comparison between original and reconstructed texts.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Preprocessed text ready for evaluation
        """
        if not self.validate_text(text):
            return text
        
        # Remove diacritical marks for fair comparison
        # (since uroman might not preserve them)
        text = self._remove_diacritics(text)
        
        # Normalize Arabic characters
        text = self._normalize_arabic_chars(text)
        
        # Handle ligatures
        text = self._handle_ligatures(text)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        return text
    
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize Arabic text into words.
        
        Arabic word boundaries can be complex due to:
        - Prefixes and suffixes
        - Clitics
        - Space-separated words
        
        Args:
            text: Input Arabic text
            
        Returns:
            List of word tokens
        """
        if not self.validate_text(text):
            return []
        
        # Basic word tokenization for Arabic
        # This is a simplified approach - more sophisticated Arabic
        # tokenization could be implemented here
        words = text.split()
        
        # Filter out empty strings and normalize
        words = [word.strip() for word in words if word.strip()]
        
        return words
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize Arabic text according to Arabic conventions.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Normalized Arabic text
        """
        if not self.validate_text(text):
            return text
        
        # Normalize Arabic characters to standard forms
        text = self._normalize_arabic_chars(text)
        
        # Normalize whitespace
        text = self._normalize_whitespace(text)
        
        # Remove extra punctuation
        text = self._clean_punctuation(text)
        
        return text
    
    def get_language_characteristics(self) -> Dict[str, Any]:
        """
        Get Arabic-specific characteristics that affect evaluation.
        
        Returns:
            Dictionary containing Arabic language characteristics
        """
        return {
            'script': 'Arabic',
            'direction': 'rtl',  # Right-to-left
            'has_diacritics': True,
            'has_ligatures': True,
            'word_boundary_type': 'space',
            'case_sensitive': False,  # Arabic doesn't have case
            'diacritic_removal': True,  # We remove diacritics for evaluation
            'ligature_handling': True
        }
    
    def _remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritical marks from text."""
        return self.diacritics.sub('', text)
    
    def _normalize_arabic_chars(self, text: str) -> str:
        """Normalize Arabic characters to standard forms."""
        # This is a basic implementation
        # More sophisticated Arabic normalization could be added here
        return text
    
    def _handle_ligatures(self, text: str) -> str:
        """Handle Arabic ligatures in text."""
        # This is a placeholder - actual ligature handling
        # would depend on the specific evaluation requirements
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace in Arabic text."""
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    def _clean_punctuation(self, text: str) -> str:
        """Clean punctuation in Arabic text."""
        # Remove extra punctuation marks
        text = re.sub(r'[،؛]+', '،', text)  # Normalize Arabic punctuation
        return text
    
    def validate_text(self, text: str) -> bool:
        """
        Validate that text contains Arabic characters.
        
        Args:
            text: Text to validate
            
        Returns:
            True if text contains Arabic characters
        """
        if not text or not isinstance(text, str):
            return False
        
        # Check if text contains Arabic characters
        return bool(self.arabic_chars.search(text))
    
    def get_evaluation_parameters(self) -> Dict[str, Any]:
        """
        Get Arabic-specific parameters for evaluation.
        
        Returns:
            Dictionary containing Arabic evaluation parameters
        """
        base_params = super().get_evaluation_parameters()
        base_params.update({
            'script_info': self.script_info,
            'diacritic_removal': True,
            'ligature_handling': True,
            'arabic_specific': True
        })
        return base_params
