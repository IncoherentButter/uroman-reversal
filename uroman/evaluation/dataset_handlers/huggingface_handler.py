"""
HuggingFace dataset handler for evaluation framework.

This handler provides functionality to load and process HuggingFace datasets
for use in uroman reverse evaluation, with special support for the
101 Billion Arabic Words Dataset.
"""

from typing import List, Dict, Any, Optional, Iterator
import logging
from datasets import Dataset, load_dataset
from ..language_adapters.base_adapter import BaseLanguageAdapter


class HuggingFaceDatasetHandler:
    """
    Handler for HuggingFace datasets used in evaluation.
    
    This class provides methods to load, filter, and process datasets
    for evaluation purposes, with support for different languages and
    dataset formats.
    """
    
    def __init__(self, dataset_name: str, language_adapter: Optional[BaseLanguageAdapter] = None):
        """
        Initialize the dataset handler.
        
        Args:
            dataset_name: Name of the HuggingFace dataset
            language_adapter: Optional language adapter for preprocessing
        """
        self.dataset_name = dataset_name
        self.language_adapter = language_adapter
        self.dataset: Optional[Dataset] = None
        self.logger = logging.getLogger(__name__)
        
        # Default configuration for the Arabic dataset
        self.default_config = {
            'max_samples': 10000,  # Limit for testing
            'text_column': 'text',
            'date_column': 'date',
            'min_text_length': 10,
            'max_text_length': 1000
        }
    
    def load_dataset(self, 
                    split: str = 'train',
                    config: Optional[Dict[str, Any]] = None) -> Dataset:
        """
        Load the specified dataset from HuggingFace.
        
        Args:
            split: Dataset split to load (e.g., 'train', 'test', 'validation')
            config: Optional configuration overrides
            
        Returns:
            Loaded HuggingFace dataset
        """
        try:
            self.logger.info(f"Loading dataset: {self.dataset_name} (split: {split})")
            
            # Load the dataset
            self.dataset = load_dataset(self.dataset_name, split=split)
            
            # Apply configuration
            if config:
                self.default_config.update(config)
            
            self.logger.info(f"Successfully loaded {len(self.dataset)} samples")
            return self.dataset
            
        except Exception as e:
            self.logger.error(f"Failed to load dataset: {e}")
            raise
    
    def filter_dataset(self, 
                      filters: Optional[Dict[str, Any]] = None) -> Dataset:
        """
        Filter the loaded dataset based on specified criteria.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            Filtered dataset
        """
        if self.dataset is None:
            raise ValueError("No dataset loaded. Call load_dataset() first.")
        
        filtered_dataset = self.dataset
        
        # Apply text length filters
        if self.default_config['min_text_length'] > 0:
            filtered_dataset = filtered_dataset.filter(
                lambda x: len(x[self.default_config['text_column']]) >= self.default_config['min_text_length']
            )
        
        if self.default_config['max_text_length'] > 0:
            filtered_dataset = filtered_dataset.filter(
                lambda x: len(x[self.default_config['text_column']]) <= self.default_config['max_text_length']
            )
        
        # Apply custom filters
        if filters:
            for key, value in filters.items():
                if key in filtered_dataset.column_names:
                    if isinstance(value, (list, tuple)):
                        filtered_dataset = filtered_dataset.filter(lambda x: x[key] in value)
                    else:
                        filtered_dataset = filtered_dataset.filter(lambda x: x[key] == value)
        
        # Limit number of samples
        if self.default_config['max_samples'] > 0:
            filtered_dataset = filtered_dataset.select(range(min(len(filtered_dataset), self.default_config['max_samples'])))
        
        self.logger.info(f"Filtered dataset: {len(filtered_dataset)} samples remaining")
        return filtered_dataset
    
    def get_text_samples(self, 
                        dataset: Optional[Dataset] = None,
                        column: Optional[str] = None) -> List[str]:
        """
        Extract text samples from the dataset.
        
        Args:
            dataset: Dataset to extract from (uses loaded dataset if None)
            column: Text column name (uses default if None)
            
        Returns:
            List of text samples
        """
        if dataset is None:
            dataset = self.dataset
        
        if dataset is None:
            raise ValueError("No dataset available")
        
        column = column or self.default_config['text_column']
        
        if column not in dataset.column_names:
            raise ValueError(f"Column '{column}' not found in dataset")
        
        texts = dataset[column]
        
        # Apply language-specific preprocessing if adapter is available
        if self.language_adapter:
            texts = [self.language_adapter.preprocess_for_evaluation(text) for text in texts]
        
        return texts
    
    def get_sample_batches(self, 
                          batch_size: int = 100,
                          dataset: Optional[Dataset] = None) -> Iterator[List[str]]:
        """
        Get text samples in batches for processing.
        
        Args:
            batch_size: Number of samples per batch
            dataset: Dataset to process (uses loaded dataset if None)
            
        Yields:
            Batches of text samples
        """
        if dataset is None:
            dataset = self.dataset
        
        if dataset is None:
            raise ValueError("No dataset available")
        
        total_samples = len(dataset)
        
        for i in range(0, total_samples, batch_size):
            end_idx = min(i + batch_size, total_samples)
            batch_dataset = dataset.select(range(i, end_idx))
            batch_texts = self.get_text_samples(batch_dataset)
            yield batch_texts
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded dataset.
        
        Returns:
            Dictionary containing dataset information
        """
        if self.dataset is None:
            return {'status': 'No dataset loaded'}
        
        info = {
            'dataset_name': self.dataset_name,
            'total_samples': len(self.dataset),
            'columns': self.dataset.column_names,
            'features': str(self.dataset.features),
            'split': getattr(self.dataset, 'split', 'unknown'),
            'config': self.default_config
        }
        
        # Add language-specific info if adapter is available
        if self.language_adapter:
            info['language'] = self.language_adapter.language_code
            info['language_characteristics'] = self.language_adapter.get_language_characteristics()
        
        return info
    
    def save_filtered_dataset(self, 
                             output_path: str,
                             dataset: Optional[Dataset] = None) -> None:
        """
        Save the filtered dataset to disk.
        
        Args:
            output_path: Path to save the dataset
            dataset: Dataset to save (uses loaded dataset if None)
        """
        if dataset is None:
            dataset = self.dataset
        
        if dataset is None:
            raise ValueError("No dataset available")
        
        try:
            dataset.save_to_disk(output_path)
            self.logger.info(f"Dataset saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save dataset: {e}")
            raise
