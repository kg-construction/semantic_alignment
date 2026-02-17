"""Ollama API client for text generation."""

import os
import requests

# Handle both relative and absolute imports
if os.environ.get('_RUNNING_AS_SCRIPT') == '1':
    from config.diplomat_config import DiplomatConfig
else:
    from ..config.diplomat_config import DiplomatConfig


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, config: DiplomatConfig):
        """
        Initialize Ollama client.
        
        Args:
            config: Diplomat configuration containing Ollama settings
        """
        self.config = config

    def generate_text(self, prompt: str) -> str:
        """
        Generate text using Ollama API.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated text string
            
        Raises:
            requests.HTTPError: If the API request fails
        """
        payload = {
            "model": self.config.llama_model,
            "prompt": prompt,
            "stream": False  # easier to parse for evaluation
        }

        response = requests.post(self.config.ollama_url, json=payload, timeout=120)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            details = self._extract_error_message(response)
            raise requests.HTTPError(
                f"Ollama request failed ({response.status_code}): {details}",
                response=response,
            ) from exc

        data = response.json()
        generated = data.get("response", "")

        return generated.strip()

    @staticmethod
    def _extract_error_message(response: requests.Response) -> str:
        try:
            data = response.json()
            if isinstance(data, dict):
                return str(data.get("error") or data.get("message") or data)
            return str(data)
        except ValueError:
            body = (response.text or "").strip()
            return body if body else "Unknown error returned by Ollama."

