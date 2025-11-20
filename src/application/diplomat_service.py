"""Diplomat service: orchestrates triple-to-text generation and evaluation."""

import os
from typing import List, Optional

# Handle both relative and absolute imports
if os.environ.get('_RUNNING_AS_SCRIPT') == '1':
    from domain.types import Triplet
    from config.diplomat_config import DiplomatConfig
    from infrastructure.ollama_client import OllamaClient
    from infrastructure.bleurt_evaluator import BLEURTEvaluator
    from infrastructure.prompt_builder import PromptBuilder
else:
    from ..domain.types import Triplet
    from ..config.diplomat_config import DiplomatConfig
    from ..infrastructure.ollama_client import OllamaClient
    from ..infrastructure.bleurt_evaluator import BLEURTEvaluator
    from ..infrastructure.prompt_builder import PromptBuilder


class DiplomatService:
    """
    Diplomat service: connects structured triples → LLM → BLEURT evaluation.
    
    This service orchestrates the pipeline:
    1. Receives triples (subject, predicate, object) and a base text
    2. Sends a prompt to Ollama's /api/generate endpoint
    3. Compares the generated text with a reference using BLEURT
    """

    def __init__(self, config: Optional[DiplomatConfig] = None):
        """
        Initialize Diplomat service.
        
        Args:
            config: Diplomat configuration (uses default if not provided)
        """
        self.config = config or DiplomatConfig()
        self.ollama_client = OllamaClient(self.config)
        self.bleurt_evaluator = BLEURTEvaluator(self.config)
        self.prompt_builder = PromptBuilder()

    def generate_text(self, triples: List[Triplet], base_text: str) -> str:
        """
        Generate text from triples using LLM.
        
        Args:
            triples: List of (subject, predicate, object) tuples
            base_text: Base text for style reference
            
        Returns:
            Generated text string
        """
        prompt = self.prompt_builder.build_prompt(triples, base_text)
        return self.ollama_client.generate_text(prompt)

    def evaluate_text(self, reference: str, candidate: str) -> float:
        """
        Evaluate candidate text against reference using BLEURT.
        
        Args:
            reference: Reference text
            candidate: Candidate text to evaluate
            
        Returns:
            BLEURT score as float
        """
        return self.bleurt_evaluator.compute_score(reference, candidate)

    def run_pipeline(
        self,
        triples: List[Triplet],
        base_text: str,
        reference_text: str
    ) -> dict:
        """
        Run the full pipeline: generate text from triples and evaluate it.
        
        Args:
            triples: List of (subject, predicate, object) tuples
            base_text: Base text for style reference
            reference_text: Reference text for evaluation
            
        Returns:
            Dictionary containing:
                - generated_text: The generated text
                - reference_text: The reference text
                - bleurt_score: The BLEURT evaluation score
        """
        generated_text = self.generate_text(triples, base_text)
        bleurt_score = self.evaluate_text(reference_text, generated_text)

        return {
            "generated_text": generated_text,
            "reference_text": reference_text,
            "bleurt_score": bleurt_score,
        }

