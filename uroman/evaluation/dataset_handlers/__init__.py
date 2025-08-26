"""
Dataset handlers for evaluation framework.

This module contains classes for handling different types of datasets
used in evaluation, including HuggingFace datasets and custom datasets.
"""

from .huggingface_handler import HuggingFaceDatasetHandler

__all__ = [
    'HuggingFaceDatasetHandler',
]
