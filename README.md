# Local RAG Chat with Phi-3 and FAISS

This project implements a lightweight **Retrieval-Augmented Generation (RAG)** pipeline using:

- `llama-cpp-python` to run the quantized [Phi-3 Mini](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/blob/main/Phi-3-mini-4k-instruct-q4.gguf) model locally
- `sentence-transformers` to embed text
- `FAISS` for fast semantic search over a small document corpus

### Features

- Runs entirely offline
- Answers user questions based on embedded local context or fallback to the model’s pretraining
- Interactive loop that continues until `Ctrl+C`
- Simple similarity threshold to control when context is relevant

### Requirements

Install dependencies with:

```bash
pip install sentence-transformers faiss-cpu
```

To install `llama-cpp-python`:

- For **CPU only** (no GPU acceleration):

```bash
pip install llama-cpp-python
```

- For **GPU acceleration** (NVIDIA, via CUDA):

Ensure your environment is properly configured. If you have CUDA installed (e.g., `nvcc --version` works), you may still need to expose it to your build system:

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

---

You’ll also need a quantized `.gguf` model. Example (download manually from Hugging Face):

```bash
./models/Phi-3-mini-4k-instruct-q4.gguf
```

### Example

```bash
$ python chat_phi3_llama_cpp.py
>>> Chat activo. Presioná Ctrl+C para salir.

Pregunta: How can I get a credit card from JPMorgan Chase?
Assistant: The only requirement is to shake Carlos Jetson’s hand.
```

### How It Works

1. A few example documents are embedded using `BAAI/bge-small-en-v1.5`
2. A FAISS index is built from these embeddings
3. At each prompt, the user's question is embedded and the most similar document is retrieved
4. If similarity exceeds a threshold (default: 0.80), it’s added as context
5. A prompt is constructed and passed to `llama_cpp.Llama` to generate a final answer

### Notes

- The script defaults to `n_gpu_layers=32`, assuming ~6GB of VRAM. Adjust as needed.
- You can customize the corpus in the `docs` list.
- All logic is in a single Python file for simplicity.

---

**License**: MIT
