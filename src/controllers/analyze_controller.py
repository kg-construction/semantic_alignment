from flask import Blueprint, jsonify, request
import requests

from ..application.analyze_service import SemanticAlignmentService
from ..domain.models import AnalyzeRequest


def create_analyze_blueprint(service: SemanticAlignmentService) -> Blueprint:
    blueprint = Blueprint("analyze", __name__)

    @blueprint.route("/health", methods=["GET"])
    def health() -> tuple:
        return jsonify({"status": "ok"}), 200

    @blueprint.route("/analyze", methods=["POST"])
    def analyze() -> tuple:
        data = request.get_json(silent=True) or {}
        text = data.get("text")
        rdf = data.get("rdf")

        if not text:
            return jsonify({"error": "Field 'text' is required."}), 400
        if not rdf:
            return jsonify({"error": "Field 'rdf' is required."}), 400

        try:
            response = service.analyze(AnalyzeRequest(text=text, rdf=rdf))
        except requests.RequestException as exc:
            return jsonify({"error": "Failed to generate response from model.", "details": str(exc)}), 502
        except RuntimeError as exc:
            return jsonify({"error": str(exc)}), 502
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(response.to_dict()), 200

    return blueprint
