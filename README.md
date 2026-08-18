# Agentic AI & RAG Engineering — Weeks 1 to 3 Reference Implementation

**Author:** Narayanan Palani  
**Scope:** Course implementation reference for Weeks 1 through 3 covering Agentic Systems, Pydantic data validation, Async execution pipelines, and local database persistence.

---

## 📁 Repository Notebooks

This repository contains two primary implementation notebooks corresponding to cloud-based and fully local execution architectures:

1. **`agentic_ai_rag_openai_v1.ipynb`**
   * **Backend:** Cloud OpenAI API (`gpt-4o-mini`)
   * **Focus:** Cloud API authentication, environment variable loading via `python-dotenv`, Pydantic data schemas, structured LLM outputs, and baseline RAG execution.

2. **`agentic_ai_rag_ollama_v2.ipynb`**
   * **Backend:** Local Ollama Service (`gpt-oss:20b`)
   * **Focus:** Zero-cost local inference, asynchronous pipeline concurrency with `asyncio`, SQLite database persistence with WAL mode, exponential backoff retries, and structured JSON logging.

---

## 🛠️ Tech Stack & Tools Used

* **Language:** Python 3.10+
* **LLM Providers:**
  * **Cloud:** OpenAI API (`gpt-4o-mini`)
  * **Local:** Ollama Service (`gpt-oss:20b`)
* **Data Validation & Schemas:** Pydantic v2
* **Concurrency & Execution:** Python `asyncio` (`asyncio.gather`, exponential retry backoff, thread offloading via `asyncio.to_thread`)
* **Storage & Persistence:** SQLite3 (with Write-Ahead Logging / `WAL` mode and `asyncio.Lock`)
* **Environment Management:** `python-dotenv`
* **Logging:** Structured JSON logging (`logging`, `json`)
* **Testing:** Pytest / `pytest-asyncio`

---

## ⚙️ Prerequisites & Installation

### 1. Python Environment Setup
Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install openai ollama pydantic python-dotenv nest-asyncio httpx pytest
```

---

### 2. Local Ollama Setup (For `agentic_ai_rag_ollama_v2.ipynb`)

To run the local version of the notebook using Ollama:

1. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. **Start the Ollama Daemon:**
   ```bash
   ollama serve
   ```
3. **Pull the required local model:**
   ```bash
   ollama pull gpt-oss:20b
   ```

---

### 3. Environment Variables Configuration (For `agentic_ai_rag_openai_v1.ipynb`)

To run the OpenAI version, create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here
```

---

## 📂 Notebook Feature Comparison

| Feature / Aspect | `agentic_ai_rag_openai_v1.ipynb` | `agentic_ai_rag_ollama_v2.ipynb` |
| :--- | :--- | :--- |
| **LLM Model** | `gpt-4o-mini` | `gpt-oss:20b` |
| **Execution Host** | OpenAI Cloud API | Local Ollama Engine |
| **API Key Required** | Yes (`OPENAI_API_KEY`) | No (100% Offline / Local) |
| **Concurrency** | Synchronous / Basic Async | High-throughput `asyncio.gather` |
| **Persistence** | In-Memory / File-based | SQLite3 Database (WAL Mode) |
| **Logging** | Console Standard Output | Structured JSON Logger |
| **Error Handling** | Basic Exceptions | Exponential Retry Backoff |

---

## 🚀 Key Configurations & Architectural Principles

### 1. SQLite Concurrency Fix (WAL Mode & Async Lock)
When running concurrent LLM calls using `asyncio.gather`, multiple tasks attempt to write to SQLite simultaneously, causing `sqlite3.OperationalError: database is locked`.

**Fix applied in `agentic_ai_rag_ollama_v2.ipynb`:**
* Enabled **Write-Ahead Logging (WAL)**: `PRAGMA journal_mode=WAL;`
* Set a **connection timeout**: `sqlite3.connect("results.db", timeout=20.0)`
* Applied `asyncio.Lock()` around database writes.
* Offloaded synchronous blocking database writes to worker threads via `asyncio.to_thread()`.

### 2. Reasoning Model Token Budgeting (`num_predict`)
Local reasoning models generate hidden `<think>` tokens prior to the final response text. Setting `num_predict` too low (e.g., `5`) will exhaust the token limit during reasoning, resulting in empty outputs.
* **Fix:** Set `num_predict` to at least `250–1000` tokens in Ollama generation options.
