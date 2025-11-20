"""
Semantic Evaluation - Knowledge Graph Triple-to-Text Conversion

This module:
1. Receives triples (subject, predicate, object) and a base text.
2. Sends a prompt to Ollama's /api/generate endpoint.
3. Compares the generated text with a reference using BLEURT.

Usage:
    python main.py
"""

import sys
from pathlib import Path

# Add current directory to path when running as script
if __name__ == "__main__":
    current_dir = Path(__file__).parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Set flag to indicate script execution
    import os
    os.environ['_RUNNING_AS_SCRIPT'] = '1'

# Import after path setup
try:
    # Try relative imports first (when used as module)
    from .application.diplomat_service import DiplomatService
    from .config.diplomat_config import DiplomatConfig
except (ImportError, ValueError):
    # Fall back to absolute imports (when run as script)
    from src.application.diplomat_service import DiplomatService
    from src.config.diplomat_config import DiplomatConfig


# -----------------------
# Example usage
# -----------------------

if __name__ == "__main__":
    triples_example = [
        ("The university", "offers", "undergraduate programs"),
        ("The programs", "aim at", "critical student formation"),
        ("The institution", "implements", "continuous self-evaluation")
    ]

    base_text = (
        "The university provides broad academic programs guided by ongoing "
        "self-evaluation and a commitment to student development."
    )

    reference = (
        "The university offers academic programs focused on critical student "
        "development and supported by continuous institutional self-assessment."
    )

    config = DiplomatConfig(
        llama_model="llama3",
        ollama_url="http://localhost:11434/api/generate",
        bleurt_model_name="Elron/bleurt-large-512"
    )

    diplomat = DiplomatService(config)

    result = diplomat.run_pipeline(triples_example, base_text, reference)

    print("Generated:", result["generated_text"])
    print("Reference:", result["reference_text"])
    print("BLEURT:", result["bleurt_score"])
