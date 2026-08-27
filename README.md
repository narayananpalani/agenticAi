# 🤖 Agentic AI & RAG Engineering 🚀✨

**👨‍💻 Author:** Narayanan Palani  
**🎯 Scope:** Course implementation reference covering Agentic Systems, Pydantic data validation, Async execution pipelines, local database persistence, testing, and full-stack integration. 

---

## 📁 Repository Notebooks & Assets 🗂️

This repository contains essential implementation notebooks and datasets corresponding to cloud-based and fully local execution architectures. 

Here is what you will find inside:

### ☁️ Cloud & Core Local Notebooks 🖥️
1. **`agentic_ai_rag_openai_v1.ipynb`** 🌐
   * **Backend:** Cloud OpenAI API (`gpt-4o-mini`)
   * **Focus:** Cloud API authentication, environment variable loading via `python-dotenv`, Pydantic data schemas, structured LLM outputs, and baseline RAG execution.

2. **`agentic_ai_rag_ollama_v2.ipynb`** 🦙
   * **Backend:** Local Ollama Service (`gpt-oss:20b`)
   * **Focus:** Zero-cost local inference, asynchronous pipeline concurrency with `asyncio`, SQLite database persistence with WAL mode, exponential backoff retries, and structured JSON logging.

### ✨ NEW: AI Engineering Course Assets 🎓
These recently added files supercharge your learning and testing pipelines:

3. **`rag_ollama_pydanticValidations_v2_2_2.ipynb`** 🛡️📓
   * **Backend:** Python, Ollama (`gpt-oss:20b`), Pydantic v2, FastAPI, Streamlit, and Pytest.
   * **Capabilities for the AI Engineer:**
     * **Interview Prep:** Features built-in *Frequently Asked Interview Questions* directly integrated into the Markdown commentary between relevant code blocks.
     * **End-to-End Pipeline:** Guides you through setting up real-time FastAPI token streaming and consuming it progressively within a Streamlit frontend UI.
     * **Resilience & Testing:** Provides robust examples of unit testing asynchronous LLM functions without triggering time-consuming inferences using `unittest.mock.AsyncMock`.
     * **Guardrails:** Demonstrates how to use Pydantic to enforce anti-hallucination guardrails, completely rejecting outputs that hallucinate data context. 

4. **`retail_payment_records.json`** 💳📊
   * **Focus:** A rich, 150-record mock dataset for stress-testing RAG data ingestion and LLM contextual grounding.
   * **Capabilities for the AI Engineer:**
     * **Validation Stress-Testing:** Perfectly crafted for testing Pydantic error handling, featuring realistic anomalies like corrupted timestamps.
     * **Edge Case Handling:** Includes challenging data points like negative transaction amounts and `null` store locations. 
     * **Grounding & Aggregation:** Provides varied combinations of currencies (USD, EUR, INR, GBP, YEN), payment methods, and success statuses to evaluate how accurately your agentic pipeline filters and categorizes raw context.

---

## 🛠️ Tech Stack & Tools Used 🧰

* **Language:** Python 3.10+ 🐍
* **LLM Providers:**
  * **Cloud:** OpenAI API (`gpt-4o-mini`) ☁️
  * **Local:** Ollama Service (`gpt-oss:20b`) 🦙
* **Data Validation & Schemas:** Pydantic v2 🛡️
* **Concurrency & Execution:** Python `asyncio` (`asyncio.gather`, exponential retry backoff, thread offloading via `asyncio.to_thread`) ⚡
* **Storage & Persistence:** SQLite3 (with Write-Ahead Logging / `WAL` mode and `asyncio.Lock`) 💾
* **Environment Management:** `python-dotenv` 🔐
* **Logging:** Structured JSON logging (`logging`, `json`) 📜
* **Web & UI Frontend:** FastAPI & Streamlit 🌐
* **Testing:** Pytest / `pytest-asyncio` / `AsyncMock` 🧪

---

## ⚙️ Prerequisites & Installation 🔌

### 1. Python Environment Setup 🐍
Create a virtual environment and install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install openai ollama pydantic python-dotenv nest-asyncio httpx pytest fastapi streamlit

```

---

### 2. Local Ollama Setup (For Local Notebooks) 🦙

To run the local version of the notebook using Ollama:

1. **Install Ollama:**
```bash
curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh

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

### 3. Environment Variables Configuration (For OpenAI version) 🔑

To run the OpenAI version, create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-proj-your-actual-api-key-here

```

---

## 📂 Notebook Feature Comparison ⚖️

| Feature / Aspect | Cloud Notebook (`_v1`) ☁️ | Local / Course Notebooks (`_v2`, `rag_ollama...`) 🦙 |
| --- | --- | --- |
| **LLM Model** | `gpt-4o-mini` | `gpt-oss:20b` |
| **Execution Host** | OpenAI Cloud API | Local Ollama Engine |
| **API Key Required** | Yes (`OPENAI_API_KEY`) | No (100% Offline / Local) |
| **Concurrency** | Synchronous / Basic Async | High-throughput `asyncio.gather` / `as_completed` |
| **Persistence** | In-Memory / File-based | SQLite3 Database (WAL Mode) |
| **Web Service** | None | FastAPI (StreamingResponse) |
| **Error Handling** | Basic Exceptions | Exponential Retry Backoff |

---

## 🚀 Key Configurations & Architectural Principles 🏗️

### 1. SQLite Concurrency Fix (WAL Mode & Async Lock) 🔒

When running concurrent LLM calls using `asyncio.gather`, multiple tasks attempt to write to SQLite simultaneously, causing `sqlite3.OperationalError: database is locked`.

**Fix applied in Local Notebooks:**

* Enabled **Write-Ahead Logging (WAL)**: `PRAGMA journal_mode=WAL;`
* Set a **connection timeout**: `sqlite3.connect("results.db", timeout=20.0)`
* Applied `asyncio.Lock()` around database writes.
* Offloaded synchronous blocking database writes to worker threads via `asyncio.to_thread()`.

### 2. Reasoning Model Token Budgeting (`num_predict`) 🧠

Local reasoning models generate hidden `<think>` tokens prior to the final response text. Setting `num_predict` too low (e.g., `5`) will exhaust the token limit during reasoning, resulting in empty outputs.

* **Fix:** Set `num_predict` to at least `250–1000` tokens in Ollama generation options.

### 3. Pydantic Anti-Hallucination Guardrails 🛡️

Instead of relying solely on prompt engineering, the new architecture performs exclusive runtime validation. The pipeline parses the LLM's JSON payload and compares cited `referenced_txn_ids` against the provided RAG context, strictly raising a `ValueError` if hallucinated contexts are detected.

---

## 🕵️‍♂️ Pydantic Data Validations: Requests vs. Responses ⚖️

This repository heavily utilizes Pydantic v2 to enforce strict data contracts across the pipeline. Here is a breakdown of how inputs and outputs are validated:

### 📥 Input Request Validations

* The `QuestionRequest` schema enforces that the user `query` must be a string with a minimum length of 3 (`min_length=3`).
* The `TransactionRecord` schema sets `model_config = ConfigDict(extra='forbid')`, strictly rejecting any unrecognized keys found in the incoming raw RAG JSON data.
* A custom `@field_validator` on the `amount` field catches and raises a `ValueError` if a negative transaction amount is detected.
* A custom `@field_validator` on the `timestamp` field throws a `ValueError` if it detects a corrupted timestamp format, such as the string `"Bad-Time"`.

### 📤 Output Response Validations & Guardrails

* The `AnswerResponse` schema strictly types the standard API outputs, requiring an `id` (int), `query` (str), `answer` (str), and a `status` (defaulting to `"success"`).
* The `LLMResponseSchema` ensures that the `confidence_score` returned by the LLM is a float strictly between 0.0 and 1.0 (`ge=0.0, le=1.0`).
* A `@field_validator` on the `answer_summary` strips whitespace and raises a `ValueError` if the LLM generates an empty answer string.
* The runtime validation engine extracts the JSON payload from the LLM, parses it into the `LLMResponseSchema`, and runs an anti-hallucination check.
* The engine validates that every ID in `referenced_txn_ids` explicitly exists in the `valid_ids_context`, raising a `ValueError` for "Hallucination Detected!" if an LLM invents an ID.

---

## 🎯 30 Essential Interview Questions & Answers for AI, RAG & MLOps Engineers 💡

### 🤖 Agentic AI & Core LLM Engineering

#### Q1: How do you measure the computational cost or token generation of a local inference request using Ollama?

> **Answer:** You extract the `prompt_eval_count` (number of input tokens evaluated) and `eval_count` (number of output tokens generated) attributes directly from the response object using Python's `getattr(response, "prompt_eval_count", 0)` and `getattr(response, "eval_count", 0)`. Summing these gives the total processed token count per request.

#### Q2: What is the significance of the `num_predict` parameter when using local reasoning models, and what happens if it is set too low?

> **Answer:** `num_predict` sets the maximum token output cap for generation. Local reasoning models generate internal `<think>` reasoning tokens before producing the final user response. If `num_predict` is set too low (e.g., `< 50`), the token budget gets exhausted during reasoning, causing empty or truncated responses.

#### Q3: How can you programmatically verify that a specific LLM model is available locally before executing prompts?

> **Answer:** Query the local Ollama daemon using `ollama.list()` to fetch installed models. Map over `[model.model for model in models.models]` to check for the required string (e.g., `gpt-oss:20b`), and raise a `RuntimeError` before running prompt execution if missing.

#### Q4: What are the key differences between synchronous and asynchronous LLM API calls, and when would you use each?

> **Answer:** Synchronous calls block the executing thread until the model generates the complete response, making them suitable for sequential scripts or simple CLI tools. Asynchronous calls (`AsyncClient`) yield execution control during network I/O wait, enabling hundreds of concurrent prompts to run simultaneously via `asyncio.gather` without freezing application threads.

#### Q5: Explain how to implement exponential backoff for LLM API retries and why it is critical for resilient systems.

> **Answer:** Wrap the async call in a retry loop (e.g., `for attempt in range(max_retries)`). On catching a transient exception, delay execution by `await asyncio.sleep(2 ** attempt)` seconds before retrying. This prevents retry storms that overwhelm recovering local daemons or trigger cloud API rate limit blocks.

#### Q6: How do you construct a system prompt to enforce strict JSON output from an LLM?

> **Answer:** Pass a system message establishing a strict role (e.g., *"You are a strict data assistant. Respond ONLY using a JSON object with this exact structure..."*) accompanied by explicit key names, data types, and formatting constraints, followed by Pydantic schema verification on output.

#### Q7: What are the benefits of running local LLMs (like `gpt-oss:20b`) over cloud-based APIs like OpenAI's?

> **Answer:** Local LLMs offer zero per-token API costs, full data privacy and sovereignty (sensitive data never leaves local infrastructure), offline capability, and protection against cloud vendor service outages or strict rate limits.

#### Q8: How do you unit test an asynchronous LLM function without triggering actual, time-consuming model inference?

> **Answer:** Use `unittest.mock.AsyncMock()` to build a fake client and response payload. Configure `mock_client.chat.return_value = mock_completion`, execute the function under test using `@pytest.mark.asyncio`, and verify execution using `mock_client.chat.assert_called_once()`.

#### Q9: What is an Architectural Decision Record (ADR), and why is it useful when defining API contracts for LLMs?

> **Answer:** An ADR is a formal document capturing an architectural decision, its context, and consequences. In LLM microservices, ADRs lock down API specs (e.g., requiring JSON schemas for `/v1/ask`), ensuring client UI apps and backend LLM pipelines maintain strict contract compatibility.

#### Q10: How do you cleanly extract JSON payloads from raw markdown wrappers (e.g., `json ... `) returned by an unpredictable LLM?

> **Answer:** Use regular expressions like `re.search(r'```(?:json)?\s*(\{.*?\})\s*```', clean_text, re.DOTALL)` to extract group 1 (the bare JSON object) before passing it to `json.loads()`.

---

### 🧩 RAG Engineering & Data Guardrails (Pydantic)

#### Q11: How can Pydantic be used to enforce anti-hallucination guardrails on an LLM's output?

> **Answer:** Define an output schema (e.g., `LLMResponseSchema`) that requires the model to cite reference IDs in a list (e.g., `referenced_txn_ids`). In post-generation parsing, verify that every cited ID strictly belongs to a set of pre-validated context IDs (`valid_txn_ids`). If an ungrounded ID appears, throw a `ValueError`.

#### Q12: Explain the concept of "Exclusive Runtime Validation" in the context of RAG pipelines.

> **Answer:** It is a post-processing execution gate that sits between raw LLM generation and client output delivery. It cleans raw text, parses it into typed models, validates logical boundary constraints, and performs anti-hallucination checks, rejecting or retrying failed payloads before they hit downstream services.

#### Q13: How do you strictly prevent an LLM from hallucinating transaction IDs or document references in its final response?

> **Answer:** Extract all valid IDs from ingested context documents into a set (`valid_txn_ids`). Collect cited IDs from the LLM response, iterate through them, and raise an explicit exception if `txn_id not in valid_txn_ids`.

#### Q14: Why is it important to use `ConfigDict(extra='forbid')` in Pydantic models for raw RAG data ingestion?

> **Answer:** Setting `extra='forbid'` ensures that any unformatted, malicious, or extraneous fields present in raw context payloads trigger an immediate `ValidationError`, preventing unknown or dirty data from passing deeper into context buffers.

#### Q15: How do you handle and gracefully log validation errors when parsing raw contextual data before feeding it to an LLM?

> **Answer:** Wrap record parsing in a `try...except ValidationError` block. Append failed payloads and error messages (`[err["msg"] for err in e.errors()]`) into a `REJECTED` bucket, log structured JSON events, and continue processing valid records.

#### Q16: Describe a strategy for filtering raw context into "ACCEPTED", "REJECTED", and "IGNORED" buckets prior to RAG generation.

> **Answer:** Schema-conforming valid records go to `ACCEPTED`; records failing Pydantic validation (e.g., corrupt dates or invalid formats) fall into `REJECTED`; valid records that do not meet context eligibility business logic (e.g., failed transaction statuses) are routed to `IGNORED`.

#### Q17: What is the role of `@field_validator` in Pydantic when sanitizing RAG inputs?

> **Answer:** `@field_validator` intercepts field values during model instantiation to apply custom validation logic (e.g., rejecting negative amounts or flags like `"Bad-Time"`), raising explicit `ValueError` exceptions before model creation succeeds.

#### Q18: If an LLM returns a plain text string instead of the requested JSON schema, how should your fallback validation pipeline handle it?

> **Answer:** Catch the `json.JSONDecodeError` during parsing and construct a default fallback dictionary mapping the raw output into `answer_summary`, setting empty citation lists and a reduced fallback `confidence_score` (e.g., `0.8`).

#### Q19: How do you integrate retrieved structured context securely into the LLM system prompt?

> **Answer:** Convert accepted Pydantic records back to a sanitized JSON string via `model.model_dump()` and append it as a explicit system context message (e.g., `{"role": "system", "content": f"Context Data: {filtered_data}"}`) separated from user input.

#### Q20: Why is calculating and returning a `confidence_score` dynamically useful in agentic workflows?

> **Answer:** Dynamic confidence scores allow agentic orchestrators to set threshold rules: high-confidence responses are served directly to users, while low-confidence responses trigger fallback queries, alternative vector search tools, or human-in-the-loop review.

---

### ⚙️ MLOps, Concurrency & Backend Engineering

#### Q21: How do you handle database concurrency and avoid "database locked" errors in SQLite when processing high-volume asynchronous LLM batches?

> **Answer:** Enable Write-Ahead Logging (`PRAGMA journal_mode=WAL;`), set connection timeouts (`sqlite3.connect(..., timeout=20.0)`), protect DB writes using a global `asyncio.Lock()`, and offload blocking synchronous I/O writes to threads using `asyncio.to_thread()`.

#### Q22: What is the purpose of Write-Ahead Logging (WAL) in SQLite, and how is it activated programmatically?

> **Answer:** WAL mode improves write concurrency by appending DB modifications to a separate `-wal` file instead of directly modifying the main database file, allowing concurrent readers to access data while writes occur. It is activated via `cursor.execute("PRAGMA journal_mode=WAL;")`.

#### Q23: What is the benefit of `asyncio.gather` versus `asyncio.as_completed` in batch LLM processing pipelines?

> **Answer:** `asyncio.gather` executes tasks concurrently and returns the full result list strictly ordered by initial input position after the slowest task completes. `asyncio.as_completed` yields individual task futures as soon as each finishes, enabling immediate low-latency streaming output or UI rendering.

#### Q24: How do you offload blocking synchronous I/O operations (like traditional database writes) in a Python `asyncio` application?

> **Answer:** Use `await asyncio.to_thread(blocking_function, *args)`. This delegates execution to a background worker thread from Python's thread pool, preventing blocking synchronous file or DB operations from stalling the main async event loop.

#### Q25: How do you implement real-time token streaming for an LLM endpoint in FastAPI?

> **Answer:** Define an `async def stream_generator(query: str)` generator that calls the client with `stream=True` and yields chunks as they arrive. Return this generator wrapped in FastAPI's `StreamingResponse(stream_generator(query), media_type="text/plain")`.

#### Q26: What is a `StreamingResponse` in FastAPI, and how does it consume an asynchronous text generator?

> **Answer:** `StreamingResponse` sends HTTP response bodies incrementally over an open HTTP connection. It consumes an async generator, streaming text chunks (using media types like `text/plain` or `text/event-stream`) directly to client connections without buffering the entire output in server memory.

#### Q27: How do you consume a streaming backend endpoint in a Streamlit interface to display progressively generated text to a user?

> **Answer:** Make an HTTP POST call with `requests.post(..., stream=True)`. Iterate over incoming chunks via `response.iter_content(chunk_size=1024, decode_unicode=True)`, append each chunk to a text buffer, and update a Streamlit placeholder using `st.empty().markdown(buffer + "▌")`.

#### Q28: Why is structured JSON logging preferred over standard console printing in production MLOps environments?

> **Answer:** Structured JSON logs serialize event metrics (e.g., `timestamp`, `event_type`, `attempt`, `token_count`) as standardized key-value pairs, making logs easily ingestable, queryable, and indexable by centralized telemetry tools like Datadog, Splunk, or AWS CloudWatch.

#### Q29: What is the purpose of a `/health` probe endpoint in a FastAPI RAG microservice?

> **Answer:** A `/health` endpoint provides an automated probe for orchestrators (like Kubernetes or Docker) to verify application readiness without invoking expensive, high-latency LLM calls.

#### Q30: How do you intentionally simulate transient network failures or API rate limits when testing an LLM pipeline's retry logic?

> **Answer:** Introduce a configurable `fail_rate` parameter (e.g., `0.3`). Before invoking the model API, evaluate `if random.random() < fail_rate:` and conditionally raise a custom `TransientError` exception to test exponential backoff and recovery handlers safely.

---

## 🤝 How to Contribute 🌟

Contributions, issues, and feature requests are very welcome! Whether you are adding new agentic evaluation benchmarks, introducing additional Pydantic guardrail schemas, or improving async pipeline concurrency, your help makes this reference repository better for everyone.

### 📜 Contribution Guidelines & Workflow

1. **Fork the Repository** 🍴
Click the **Fork** button at the top right of this repository page to create a copy under your own GitHub account.
2. **Clone Your Fork** 💻
```bash
git clone [https://github.com/narayananpalani/agenticAi.git](https://github.com/narayananpalani/agenticAi.git)
cd agenticAi

```


3. **Create a New Feature Branch** 🌿
```bash
git checkout -b feature/AmazingAgenticFeature

```


4. **Set Up the Virtual Environment & Install Dependencies** 🐍
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # Or install dependencies via pip

```


5. **Make Your Changes & Add Unit Tests** 🧪
* Ensure any new LLM features include Pydantic request/response validations.
* If adding new async calls, write non-inference unit tests using `pytest` and `AsyncMock`.
* Maintain zero-cost local execution compatibility with Ollama (`gpt-oss:20b`).


6. **Run Existing Tests** ✅
```bash
pytest

```


7. **Commit Your Changes** 📝
```bash
git commit -m "✨ Add AmazingAgenticFeature with Pydantic guardrails"

```


8. **Push to Your Branch** 🚀
```bash
git push origin feature/AmazingAgenticFeature

```


9. **Open a Pull Request (PR)** 📬
Navigate to the original repository and click **New Pull Request**. Describe your changes, outline any newly added Pydantic validations, and link any related issues!

---

## 📄 License 📜

This project is licensed under the **MIT License** — see the [LICENSE](https://www.google.com/search?q=LICENSE) file for details. You are free to use, modify, and distribute this codebase for learning, research, or commercial applications.

---

🌟 **Explore the full codebase, contribute, and connect!** 🌟

🔗 **Maintained by:** [Narayanan Palani](https://github.com/narayananpalani)

