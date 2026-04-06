import os

from flask import Flask

from .application.analyze_service import SemanticAlignmentService
from .config.diplomat_config import DiplomatConfig
from .controllers.analyze_controller import create_analyze_blueprint
from .infrastructure.ollama_client import OllamaClient
from .infrastructure.prompt_repository import PromptRepository


def create_app() -> Flask:
    app = Flask(__name__)

    config = DiplomatConfig(
        llama_model=os.getenv("OLLAMA_MODEL", os.getenv("LLAMA_MODEL", "llama3")),
        ollama_url=os.getenv("OLLAMA_API_URL", os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")),
        bleurt_model_name=os.getenv("BLEURT_MODEL_NAME", "Elron/bleurt-base-512"),
        device=os.getenv("BLEURT_DEVICE"),
    )
    ollama_client = OllamaClient(config=config)
    prompt_repository = PromptRepository()
    default_prompt = os.getenv("DEFAULT_PROMPT_NAME", "rdf-to-text.txt")
    service = SemanticAlignmentService(
        ollama_client=ollama_client,
        config=config,
        prompt_repository=prompt_repository,
        default_prompt=default_prompt,
    )
    app.register_blueprint(create_analyze_blueprint(service))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5060, debug=True)
