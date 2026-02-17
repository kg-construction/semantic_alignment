# Semantic Evaluation - Knowledge Graph Triple-to-Text Conversion

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)

Semantic evaluation system that converts knowledge graph triples into fluent text using LLMs and evaluates quality using BLEURT.

## 📋 Description

This project implements a complete pipeline that:
1. Receives knowledge graph triples (subject, predicate, object) and a base text
2. Sends a prompt to Ollama's `/api/generate` endpoint
3. Compares the generated text with a reference using the BLEURT model

The code is organized following **Domain-Driven Design (DDD)** principles to facilitate maintenance, testing, and extension.

## 🔧 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```
### 2. Install and Configure Ollama

#### Install Ollama:
- **Windows/Mac**: Download from [https://ollama.ai](https://ollama.ai)

#### Download model:
```bash
ollama pull llama3:8b
```

#### Run model
```
ollama run llama3:8b
```

#### Verify Ollama is running:
```bash
ollama serve
```

The server should be available at `http://localhost:11434`

## 🚀 Usage

### Run API

Run from the `semantic_alignment` directory:

```bash
python -m src.app
```

The API starts on `http://127.0.0.1:5060`.

### Analyze Endpoint

`POST /analyze`

Behavior:
- The LLM receives only the RDF and generates plain text (`generated_text`).
- BLEURT is calculated by comparing `generated_text` against the original `text`.
- The prompt template is loaded from `prompts/rdf-to-text.txt` (or `DEFAULT_PROMPT_NAME`).

Request body:

```json
{
  "text": "Original text",
  "rdf": "@prefix ex: <http://example.org/> ."
}
```

Response body:

```json
{
  "text": "Original text",
  "rdf": "@prefix ex: <http://example.org/> .",
  "generated_text": "Text generated from RDF.",
  "bleurt": 0.91
}
```
