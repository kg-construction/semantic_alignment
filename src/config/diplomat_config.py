"""Configuration for Diplomat service."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DiplomatConfig:
    """Configuration for Diplomat service."""

    # Ollama settings
    llama_model: str = "llama3"
    ollama_url: str = "http://localhost:11434/api/generate"

    # BLEURT model
    bleurt_model_name: str = "Elron/bleurt-base-512"
    device: Optional[str] = None  # "cuda", "cpu", or None for auto-detect

