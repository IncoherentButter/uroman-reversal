"""
Example usage of the uroman evaluation framework.

This script demonstrates how to use the evaluation framework to assess
reverse uroman performance on the Arabic dataset.
"""

import logging
from typing import List
from .base_evaluator import BaseEvaluator, EvaluationResult
from .language_adapters.arabic_adapter import ArabicAdapter
from .dataset_handlers.huggingface_handler import HuggingFaceDatasetHandler
from .results_analyzer import ResultsAnalyzer
from .metrics.word_error_rate import WordErrorRate
from .metrics.character_error_rate import CharacterErrorRate
from .metrics.match_error_rate import MatchErrorRate
from .metrics.information_metrics import InformationMetrics


class ArabicEvaluator(BaseEvaluator):
    """
    Arabic-specific evaluator that implements the abstract methods.
    
    This evaluator uses the Arabic language adapter and specific
    metrics to evaluate reverse uroman performance on Arabic text.
    """
    
    def __init__(self):
        """Initialize the Arabic evaluator."""
        super().__init__('ar')
        
        # Initialize metrics
        self.wer_metric = WordErrorRate()
        self.cer_metric = CharacterErrorRate()
        self.mer_metric = MatchErrorRate()
        self.info_metric = InformationMetrics()
        
        # Initialize language adapter
        self.language_adapter = ArabicAdapter()
    
    def evaluate_word_error_rate(self, 
                               original_texts: List[str], 
                               reconstructed_texts: List[str]) -> EvaluationResult:
        """Evaluate word error rate for Arabic texts."""
        # Preprocess texts using Arabic adapter
        processed_originals = [self.language_adapter.preprocess_for_evaluation(text) 
                             for text in original_texts]
        processed_reconstructed = [self.language_adapter.preprocess_for_evaluation(text) 
                                 for text in reconstructed_texts]
        
        # Calculate WER
        wer_results = self.wer_metric.calculate(processed_originals, processed_reconstructed)
        
        return EvaluationResult(
            metric_name="Word Error Rate",
            value=wer_results['overall_wer'],
            metadata=wer_results,
            language=self.language,
            sample_size=len(original_texts)
        )
    
    def evaluate_character_error_rate(self, 
                                   original_texts: List[str], 
                                   reconstructed_texts: List[str]) -> EvaluationResult:
        """Evaluate character error rate for Arabic texts."""
        # Preprocess texts using Arabic adapter
        processed_originals = [self.language_adapter.preprocess_for_evaluation(text) 
                             for text in original_texts]
        processed_reconstructed = [self.language_adapter.preprocess_for_evaluation(text) 
                                 for text in reconstructed_texts]
        
        # Calculate CER
        cer_results = self.cer_metric.calculate(processed_originals, processed_reconstructed)
        
        return EvaluationResult(
            metric_name="Character Error Rate",
            value=cer_results['overall_cer'],
            metadata=cer_results,
            language=self.language,
            sample_size=len(original_texts)
        )
    
    def evaluate_match_error_rate(self, 
                               original_texts: List[str], 
                               reconstructed_texts: List[str]) -> EvaluationResult:
        """Evaluate match error rate for Arabic texts."""
        # Preprocess texts using Arabic adapter
        processed_originals = [self.language_adapter.preprocess_for_evaluation(text) 
                             for text in original_texts]
        processed_reconstructed = [self.language_adapter.preprocess_for_evaluation(text) 
                                 for text in reconstructed_texts]
        
        # Calculate MER
        mer_results = self.mer_metric.calculate(processed_originals, processed_reconstructed)
        
        return EvaluationResult(
            metric_name="Match Error Rate",
            value=mer_results['overall_mer'],
            metadata=mer_results,
            language=self.language,
            sample_size=len(original_texts)
        )
    
    def evaluate_information_preservation(self, 
                                       original_texts: List[str], 
                                       reconstructed_texts: List[str]) -> EvaluationResult:
        """Evaluate information preservation for Arabic texts."""
        # Preprocess texts using Arabic adapter
        processed_originals = [self.language_adapter.preprocess_for_evaluation(text) 
                             for text in original_texts]
        processed_reconstructed = [self.language_adapter.preprocess_for_evaluation(text) 
                                 for text in reconstructed_texts]
        
        # Calculate information metrics
        info_results = self.info_metric.calculate(processed_originals, processed_reconstructed)
        
        # Use character diversity preservation rate as the main metric
        main_metric = info_results.get('character_diversity', {}).get('preservation_rate', 0.0)
        
        return EvaluationResult(
            metric_name="Information Preservation",
            value=main_metric,
            metadata=info_results,
            language=self.language,
            sample_size=len(original_texts)
        )


def main():
    """Main function demonstrating the evaluation framework."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting uroman evaluation framework demonstration")
    
    try:
        # Initialize the Arabic evaluator
        evaluator = ArabicEvaluator()
        
        # Initialize dataset handler for the Arabic dataset
        dataset_handler = HuggingFaceDatasetHandler(
            dataset_name="ClusterlabAi/101_billion_arabic_words_dataset",
            language_adapter=evaluator.language_adapter
        )
        
        # Load a small subset of the dataset for demonstration
        logger.info("Loading Arabic dataset...")
        dataset = dataset_handler.load_dataset(
            split='train',
            config={'max_samples': 1000, 'min_text_length': 20, 'max_text_length': 200}
        )
        
        # Get text samples
        original_texts = dataset_handler.get_text_samples(dataset)
        logger.info(f"Loaded {len(original_texts)} Arabic text samples")
        
        # For demonstration, we'll simulate reconstructed texts
        # In practice, you would run these through your reverse uroman system
        reconstructed_texts = simulate_reverse_uroman(original_texts)
        
        # Run evaluation
        logger.info("Running evaluation...")
        results = evaluator.run_full_evaluation(original_texts, reconstructed_texts)
        
        # Analyze results
        analyzer = ResultsAnalyzer()
        analyzer.add_results(results)
        
        # Get summary
        summary = analyzer.get_summary_statistics()
        logger.info("Evaluation Summary:")
        logger.info(f"  Total evaluations: {summary['total_evaluations']}")
        logger.info(f"  Languages: {summary['languages']}")
        logger.info(f"  Metrics: {summary['metrics']}")
        
        # Export results
        logger.info("Exporting results...")
        analyzer.export_results("evaluation_results.json", format="json")
        analyzer.export_results("evaluation_results.csv", format="csv")
        
        # Create visualizations
        logger.info("Creating visualizations...")
        analyzer.create_visualizations("evaluation_plots")
        
        logger.info("Evaluation completed successfully!")
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        raise


def simulate_reverse_uroman(texts: List[str]) -> List[str]:
    """
    Simulate reverse uroman output for demonstration purposes.
    
    In practice, you would replace this with actual calls to your
    reverse uroman system.
    
    Args:
        texts: List of original Arabic texts
        
    Returns:
        List of simulated reconstructed texts
    """
    # This is a placeholder - replace with actual reverse uroman calls
    reconstructed = []
    
    for text in texts:
        # Simulate some errors that might occur in reverse uroman
        # For demonstration, we'll introduce some random changes
        import random
        
        # Simulate character substitutions, insertions, deletions
        if random.random() < 0.1:  # 10% chance of error
            # Simulate a simple error
            if len(text) > 5:
                # Randomly change one character
                pos = random.randint(0, len(text) - 1)
                text = text[:pos] + 'X' + text[pos+1:]
        
        reconstructed.append(text)
    
    return reconstructed


if __name__ == "__main__":
    main()
