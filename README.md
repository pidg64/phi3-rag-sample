# Local RAG with Phi-3, FAISS & FastAPI

This project implements a modular **Retrieval-Augmented Generation (RAG)** pipeline powered by local LLMs like Phi-3 (via `llama-cpp`) or Qwen2-VL-7B (via `Ollama`).

- [`llama-cpp-python`](https://github.com/abetlen/llama-cpp-python) for running the quantized [Phi-3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf) model locally (CPU/GPU)
- [`sentence-transformers`](https://www.sbert.net/) for generating multilingual dense embeddings
- [`FAISS`](https://github.com/facebookresearch/faiss) for efficient vector search
- [`FastAPI`](https://fastapi.tiangolo.com/) to expose the functionality as a REST API

---

## Features

- Runs completely **offline**
- Modular Python design: CLI and HTTP API via FastAPI
- Supports both **Spanish** and **English**
- GPU acceleration via CUDA (optional)
- Retrieve context from local knowledge base (`./docs/local_kb_<es|en>.txt`)
- Interactive CLI mode for fast testing
- Environment-configurable settings
- **Switchable LLM backend**: Supports both `llama-cpp` (e.g. Phi-3) and `Ollama` (e.g. Qwen2-VL-7B)

---

## Project Structure

```
.
├── app/                # Core application modules
│   ├── api/            # FastAPI routing and dependencies
│   ├── cli/            # CLI interface for interactive chat
│   ├── core/           # Logger and global settings
│   ├── schemas/        # Pydantic schemas for API I/O
│   ├── services/       # RAGService logic (LLM + retriever)
│   └── utils/          # Prompt builder and utilities
├── docs/               # Local knowledge base
├── models/             # GGUF LLM files
├── run_api.py          # Entry point for FastAPI app
├── run_chat.py         # Entry point for CLI chat loop
```

---

## Installation

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If using GPU, reinstall `llama-cpp-python` with CUDA:

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
CMAKE_ARGS="-DGGML_CUDA=on" ./venv/bin/pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### 3. Download the model

Download the quantized Phi-3 Mini model (e.g. `q4`) into `./models/`:

```bash
./models/Phi-3-mini-4k-instruct-q4.gguf
```

---

## Run CLI chat loop

```bash
python run_chat.py
```

Example:

```bash
>>> Chat activo. Presioná Ctrl+C para salir.

Pregunta: ¿Qué necesito para abrir una cuenta en el banco?
Respuesta: Para abrir una cuenta en el banco, se requiere identificación oficial, domicilio, etc.
```

---

## Run API server

```bash
python run_api.py
```

Then POST to:

```
POST /rag/ask
```

Example payload:

```json
{
  "question": "¿Qué necesito para obtener una tarjeta de crédito?",
  "language": "es"
}
```

---

## Environment Variables

Customize behavior by setting:

| Variable                 | Default Value                               | Description                            |
| ------------------------ | ------------------------------------------- | -------------------------------------- |
| `DEBUG`                | `False`                                   | Enables debug logging                  |
| `LANGUAGE`             | `es`                                      | Default language (`es` or `en`)    |
| `SIMILARITY_THRESHOLD` | `0.80`                                    | Min similarity to include context      |
| `MODEL_PATH`           | `./models/Phi-3-mini-4k-instruct-q4.gguf` | LLM model path                         |
| `EMBEDDING_MODEL_NAME` | `intfloat/multilingual-e5-small`          | HuggingFace model for embeddings       |
| `LLM_BACKEND`          | `llama`                                   | Either `llama` or `ollama` backend |

You can use a `.env` file or export variables before running.

If `LLM_BACKEND` is set to `ollama`, the API will delegate requests to a local Ollama server (e.g. `Qwen2-VL-7B`).
Make sure Ollama is installed and running the desired model before querying:

```bash
ollama run qwen2-vl
```

---

## Notes

- Compatible with CUDA-enabled GPUs (`n_gpu_layers` configurable in `settings`)
- Documents are split line-by-line in `./docs/local_kb_es.txt` if the language is Spanish, or `./docs/local_kb_en.txt` if the language is English
- Prompt formatting is handled in `app/utils/prompt.py`
- Extend the project easily with custom document loaders or model variants

---

## License

MIT
