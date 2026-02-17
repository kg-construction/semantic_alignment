from __future__ import annotations

from pathlib import Path


class PromptRepository:
    def __init__(self, prompt_dir: Path | None = None) -> None:
        self.prompt_dir = prompt_dir or Path(__file__).resolve().parents[2] / "prompts"

    def load_prompt(self, prompt_name: str) -> str:
        prompt_path = self.prompt_dir / prompt_name
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_name}")
        return prompt_path.read_text(encoding="utf-8").strip()
