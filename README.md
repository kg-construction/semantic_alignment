# Semantic Evaluation - Knowledge Graph Triple-to-Text Conversion

![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)

Semantic evaluation system that converts knowledge graph triples into fluent text using LLMs and evaluates quality using BLEURT.

## 📋 Description

This project implements a complete pipeline that:
1. Receives knowledge graph triples (subject, predicate, object) and a base text
2. Sends a prompt to Ollama's `/api/generate` endpoint
3. Compares the generated text with a reference using the BLEURT model

The code is organized following **Domain-Driven Design (DDD)** principles to facilitate maintenance, testing, and extension.

## 🏗️ Architecture

The project is structured in layers following DDD:

```
semantic_evaluation/
├── domain/                    # Domain layer
│   └── types.py              # Domain types (Triplet)
│
├── config/                    # Configuration
│   └── diplomat_config.py    # Service configuration
│
├── infrastructure/            # Infrastructure layer
│   ├── ollama_client.py      # Ollama API client
│   ├── bleurt_evaluator.py   # BLEURT evaluator
│   └── prompt_builder.py    # Prompt builder
│
├── application/               # Application layer
│   └── diplomat_service.py  # Main service (orchestration)
│
└── main.py                   # Entry point
```

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

### Run Example

Simply run from the `semantic_evaluation` directory:

```bash
python main.py
```
