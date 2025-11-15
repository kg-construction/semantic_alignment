"""Prompt builder for knowledge graph triples to text conversion."""

import os
from typing import List

# Handle both relative and absolute imports
if os.environ.get('_RUNNING_AS_SCRIPT') == '1':
    from domain.types import Triplet
else:
    from ..domain.types import Triplet


class PromptBuilder:
    """Builds prompts for converting knowledge graph triples to fluent text."""

    @staticmethod
    def build_prompt(triples: List[Triplet], base_text: str) -> str:
        """
        Build a prompt for converting triples to text.
        
        Args:
            triples: List of (subject, predicate, object) tuples
            base_text: Base text for style reference
            
        Returns:
            Formatted prompt string
        """
        triple_lines = [f"({s}) --[{p}]--> ({o})" for s, p, o in triples]
        triple_block = "\n".join(triple_lines)

        prompt = f"""
You are a model specialized in turning knowledge graph triples into fluent text.

Triples:
{triple_block}

Base text for style (do not copy literally):
\"\"\"{base_text}\"\"\"

Rules:
- Write in English.
- Produce 1–3 coherent sentences.
- Do not mention triples or graphs.
- Output only the final text.

Generated text:
""".strip()

        return prompt

