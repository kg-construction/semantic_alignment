from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..config.diplomat_config import DiplomatConfig
from ..domain.models import AnalyzeRequest, AnalyzeResponse
from ..infrastructure.ollama_client import OllamaClient
from ..infrastructure.prompt_repository import PromptRepository

if TYPE_CHECKING:
    from ..infrastructure.bleurt_evaluator import BLEURTEvaluator

BLEURTEvaluator = None


class SemanticAlignmentService:
    def __init__(
        self,
        ollama_client: Optional[OllamaClient] = None,
        config: Optional[DiplomatConfig] = None,
        bleurt_evaluator: Optional[BLEURTEvaluator] = None,
        prompt_repository: Optional[PromptRepository] = None,
        default_prompt: str = "rdf-to-text.txt",
    ) -> None:
        self.ollama_client = ollama_client
        self.config = config
        self.bleurt_evaluator = bleurt_evaluator
        self.prompt_repository = prompt_repository or PromptRepository()
        self.default_prompt = default_prompt

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        if not self.ollama_client:
            return AnalyzeResponse(text=request.text, rdf=request.rdf, generated_text="", bleurt=0.0)

        prompt_template = self.prompt_repository.load_prompt(self.default_prompt)
        verbalization_prompt = self._build_verbalization_prompt(prompt_template, request.rdf)
        candidate_text = self.ollama_client.generate_text(verbalization_prompt).strip()
        if not candidate_text:
            raise RuntimeError("Model returned empty text for RDF verbalization.")

        bleurt_score = self._compute_bleurt(request.text, candidate_text)
        return AnalyzeResponse(text=request.text, rdf=request.rdf, generated_text=candidate_text, bleurt=bleurt_score)

    @staticmethod
    def _build_verbalization_prompt(prompt_template: str, rdf: str) -> str:
        if "${RDF}" in prompt_template:
            return prompt_template.replace("${RDF}", rdf)
        return f"{prompt_template}\n\nRDF:\n{rdf}\n"

    def _compute_bleurt(self, reference: str, candidate: str) -> float:
        evaluator = self.bleurt_evaluator
        if evaluator is None and self.config is not None:
            evaluator_cls = BLEURTEvaluator
            if evaluator_cls is None:
                from ..infrastructure.bleurt_evaluator import BLEURTEvaluator as evaluator_cls

            evaluator = evaluator_cls(config=self.config)
            self.bleurt_evaluator = evaluator
        if evaluator is None:
            raise RuntimeError("BLEURT evaluator is not configured.")
        return evaluator.compute_score(reference=reference, candidate=candidate)
