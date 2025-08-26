"""
Language adapters for evaluation framework.

This module contains language-specific adapters that handle
characteristics unique to different languages and scripts.
"""

from .base_adapter import BaseLanguageAdapter
from .arabic_adapter import ArabicAdapter

__all__ = [
    'BaseLanguageAdapter',
    'ArabicAdapter',
]
