"""BLEURT model evaluator for text similarity scoring."""

import os
import torch
from typing import Optional, Tuple
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Handle both relative and absolute imports
if os.environ.get('_RUNNING_AS_SCRIPT') == '1':
    from config.diplomat_config import DiplomatConfig
else:
    from ..config.diplomat_config import DiplomatConfig


class BLEURTEvaluator:
    """Evaluator using BLEURT model for text similarity scoring."""

    def __init__(self, config: DiplomatConfig, device: Optional[str] = None):
        """
        Initialize BLEURT evaluator.
        
        Args:
            config: Diplomat configuration containing BLEURT settings
            device: Device to use ("cuda", "cpu", or None for auto-detect)
        """
        self.config = config
        self.device = device or self._select_device()
        self.tokenizer, self.model = self._load_bleurt()

    def _select_device(self) -> str:
        """Select device (CUDA if available, otherwise CPU)."""
        if self.config.device:
            return self.config.device
        return "cuda" if torch.cuda.is_available() else "cpu"

    def _load_bleurt(self) -> Tuple[AutoTokenizer, AutoModelForSequenceClassification]:
        """Load BLEURT tokenizer and model."""
        tokenizer = AutoTokenizer.from_pretrained(self.config.bleurt_model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            self.config.bleurt_model_name
        )
        model.to(self.device)
        model.eval()
        return tokenizer, model

    def compute_score(self, reference: str, candidate: str) -> float:
        """
        Compute BLEURT score between reference and candidate text.
        
        Args:
            reference: Reference text
            candidate: Candidate text to evaluate
            
        Returns:
            BLEURT score as float
        """
        enc = self.tokenizer(
            candidate,
            reference,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        enc = {k: v.to(self.device) for k, v in enc.items()}

        with torch.no_grad():
            outputs = self.model(**enc)
            score = outputs.logits.squeeze().cpu().numpy()

        return float(score)

