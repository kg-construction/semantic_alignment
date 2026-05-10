"""Configuration for Diplomat service."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DiplomatConfig:
    """Configuration for Diplomat service."""

    # Ollama settings
    llama_model: str = "llama3"
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_timeout_seconds: float = 600.0
    ollama_max_retries: int = 3
    ollama_retry_sleep_seconds: float = 5.0
    ollama_num_predict: int = 160

    # BLEURT model
    bleurt_model_name: str = "Elron/bleurt-base-512"
    device: Optional[str] = None  # "cuda", "cpu", or None for auto-detect

