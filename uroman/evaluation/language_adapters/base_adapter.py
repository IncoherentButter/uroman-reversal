"""
Base language adapter for evaluation framework.

This abstract class defines the interface that all language-specific
adapters must implement to handle language-specific characteristics.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLanguageAdapter(ABC):
    """
    Abstract base class for language-specific adapters.
    
    Language adapters handle characteristics unique to different
    languages and scripts, such as tokenization, normalization,
    and script-specific preprocessing.
    """
    
    def __init__(self, language_code: str):
        """
        Initialize the language adapter.
        
        Args:
            language_code: ISO language code (e.g., 'ar', 'zh', 'ja')
        """
        self.language_code = language_code
        self.script_info = self._get_script_info()
    
    @abstractmethod
    def preprocess_for_evaluation(self, text: str) -> str:
        """
        Preprocess text for evaluation.
        
        This method handles language-specific preprocessing that
        ensures fair comparison between original and reconstructed texts.
        
        Args:
            text: Input text to preprocess
            
        Returns:
            Preprocessed text ready for evaluation
        """
        pass
    
    @abstractmethod
    def tokenize_words(self, text: str) -> List[str]:
        """
        Tokenize text into words according to language-specific rules.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of word tokens
        """
        pass
    
    @abstractmethod
    def normalize_text(self, text: str) -> str:
        """
        Normalize text according to language-specific conventions.
        
        Args:
            text: Input text to normalize
            
        Returns:
            Normalized text
        """
        pass
    
    @abstractmethod
    def get_language_characteristics(self) -> Dict[str, Any]:
        """
        Get language-specific characteristics that affect evaluation.
        
        Returns:
            Dictionary containing language characteristics
        """
        pass
    
    def _get_script_info(self) -> Dict[str, Any]:
        """
        Get information about the script used by this language.
        
        Returns:
            Dictionary containing script information
        """
        return {
            'direction': 'ltr',  # Default to left-to-right
            'has_diacritics': False,
            'has_ligatures': False,
            'word_boundary_type': 'space',
            'case_sensitive': True
        }
    
    def validate_text(self, text: str) -> bool:
        """
        Validate that text is appropriate for this language.
        
        Args:
            text: Text to validate
            
        Returns:
            True if text is valid for this language
        """
        if not text or not isinstance(text, str):
            return False
        
        # Basic validation - can be overridden by specific adapters
        return True
    
    def get_evaluation_parameters(self) -> Dict[str, Any]:
        """
        Get language-specific parameters for evaluation.
        
        Returns:
            Dictionary containing evaluation parameters
        """
        return {
            'language_code': self.language_code,
            'script_info': self.script_info,
            'normalization_level': 'standard',
            'tokenization_method': 'default'
        }
