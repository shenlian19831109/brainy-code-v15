# BrainyCode v1.5: Brain-Inspired Verifiable Code Generation Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

**BrainyCode** is a next-generation code generation assistant that leverages a brain-inspired dual-system architecture to eliminate AI hallucinations. By integrating a "Program Truth Layer" (Minimal IR) and a "Predictive Coding Loop," it reduces API-related hallucinations by over 80% without retraining models.

---

## 🧠 Core Philosophy: The Brain-Inspired Architecture

BrainyCode simulates the human brain's complementary learning systems to provide factual anchors during the generation process:

| Brain Region | Engineering Module | Function |
| :--- | :--- | :--- |
| **Hippocampus** | `MemoryStore` | **Episodic Memory**: Stores user preferences and forbidden patterns via vector embeddings. |
| **Neocortex** | `MinimalIR` | **Semantic Memory**: Extracts a precise symbol table (functions, params) from the source code. |
| **Prefrontal Cortex** | `ConstraintExecutor` | **Executive Control**: Monitors LLM output and triggers error signals for non-existent functions. |
| **Predictive Coding** | `Validation Loop` | **Error-Driven Correction**: A Generate → Validate → Refine cycle to ensure code reliability. |

---

## ✨ Key Features

- 🚫 **Hallucination Suppression**: Intercepts and corrects fabricated APIs in real-time.
- 📚 **Context-Aware Memory**: Automatically avoids patterns or libraries you've previously rejected.
- 🔍 **Multi-Language IR**: Supports symbol extraction for **Python**, **TypeScript**, and **JavaScript**.
- 🛠️ **LSP Guardrail**: Final syntax validation using compiler-level checks to ensure "runnable" output.
- 🔌 **Flexible Adapters**: Seamlessly switch between **Ollama** (Local), **OpenAI**, and **HuggingFace**.

---

## 🚀 Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/shenlian19831109/brainy-code-v15.git
cd brainy-code-v15

# Install core dependencies
pip install -r requirements.txt

# Install optional providers (if using OpenAI/Pydantic)
pip install openai pydantic
```

### 2. Configuration

Set up your environment variables (or use a `.env` file):

```bash
# LLM Provider (ollama, openai, huggingface_inference)
export LLM_PROVIDER=ollama
export LLM_MODEL=codestral

# Embedding Provider (openai, jina)
export EMBED_PROVIDER=openai
export OPENAI_API_KEY=sk-xxxx
```

---

## 🛠️ Usage

### Build Program Truth (IR)
Scan your project to build the local symbol table:
```bash
python cli.py build-ir --project-root /path/to/your/project
```

### Generate Verifiable Code
Generate code that is strictly constrained by your project's existing functions:
```bash
python cli.py generate --project-root . "Create a data processing pipeline using our internal logger"
```

### Teach the Assistant (Feedback)
Record preferences to the "Hippocampus" memory:
```python
from config import Config
from ai_assistant import AIAssistantV15

assistant = AIAssistantV15(Config(project_root="."))
assistant.user_feedback("Do not use the 'eval' function", accepted=False)
```

---

## 📂 Project Structure

```text
├── ai_assistant.py        # Main Orchestrator
├── cli.py                 # Command Line Interface
├── config.py              # Configuration Management
├── constraint_executor.py # Prefrontal Cortex (Validation)
├── embedding_adapter.py   # Embedding Service Wrapper
├── ir_extractor.py        # Neocortex (Symbol Extraction)
├── llm_adapter.py         # LLM Service Wrapper
├── lsp_validator.py       # Syntax Guardrail
└── memory_store.py        # Hippocampus (Vector Memory)
```

---

## 🗺️ Roadmap

- [x] **v1.5**: Minimal IR + Hard Constraints + Semi-constrained Generation (Current)
- [ ] **v2.0 alpha**: Full IR (Types, Call Graphs) + Constrained Decoding
- [ ] **v2.0 beta**: Multi-language support expansion & Private deployment optimization

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---
*Developed with ❤️ to bridge the gap between AI creativity and program truth.*
