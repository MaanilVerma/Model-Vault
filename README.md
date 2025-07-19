# MiniVault API

A lightweight, fully local REST API that simulates prompt/response behavior like
ModelVault or OpenAI—**no cloud required**. Supports local LLMs via Ollama, with a stub
fallback for universal testability.

---

## 🎥 Demo Video

See a full walkthrough of setup, stubbed and Ollama-backed responses, and API testing via CLI, Swagger, and Postman:

## [Watch the demo video on YouTube](https://www.youtube.com/watch?v=PQ7KdvKRDiI)

<iframe width="560" height="315" src="https://www.youtube.com/embed/PQ7KdvKRDiI" title="MiniVault API Demo" frameborder="0" allowfullscreen></iframe>

## 🚀 Features

- `POST /generate` — Synchronous prompt/response endpoint
- `POST /stream` — Streams output token-by-token (SSE)
- **Stub fallback** if Ollama is not running
- Logs all requests/responses to `logs/log.jsonl`
- CLI and Postman collection for easy testing
- OpenAPI docs at `/docs`

---

## 🗂️ Project Structure

```
minivault-api/
├── app.py                  # FastAPI app
├── model_handler.py        # Model/stub logic
├── log_writer.py           # Logging utility
├── cli.py                  # CLI tool (supports both /generate and /stream)
├── postman_collection.json # Postman config
├── requirements.txt        # Python dependencies
├── logs/
│   └── log.jsonl           # Log file
└── README.md               # This file
```

---

## ⚡ Quickstart

### 1. Install dependencies

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

## 🦙 Ollama Setup (macOS & Windows)

### **macOS**

1. **Download Ollama:**  
   [https://ollama.com/download](https://ollama.com/download)  
   Open the `.dmg`, drag Ollama to Applications, and **start the Ollama application** (double-click in Applications folder).
2. **Add Ollama to your PATH (if needed):**  
   If `ollama` is not found in Terminal, run:
   ```bash
   export PATH="/Applications/Ollama.app/Contents/MacOS:$PATH"
   ```
   _(Add this to your `~/.zshrc` for persistence.)_
3. **Verify installation:**
   ```bash
   ollama --version
   ```
4. **Download and run a model:**
   ```bash
   ollama run llama3
   ```
   - The first run will download the model (may take a few minutes).
   - You can interact with the model in the terminal, or just close it after the download.
5. **Ready!**
   Ollama’s API will be available at `http://localhost:11434` for your MiniVault API.

### **Windows**

1. **Download Ollama:**  
   [https://ollama.com/download](https://ollama.com/download)  
   Run the installer and **start the Ollama application** from the Start Menu.
2. **Add Ollama to your PATH (if needed):**  
   The installer should add Ollama to your PATH automatically. If not, add the install directory (e.g., `C:\Program Files\Ollama`) to your PATH manually.
3. **Open Command Prompt or PowerShell and verify installation:**
   ```bat
   ollama --version
   ```
4. **Download and run a model:**
   ```bat
   ollama run llama3
   ```
   - The first run will download the model (may take a few minutes).
5. **Ready!**
   Ollama’s API will be available at `http://localhost:11434` for your MiniVault API.

---

## 🧪 Testing Options

### CLI (supports both full and streaming responses)

#### **1. Make sure the API server is running**

```bash
uvicorn app:app --reload
```

#### **2. In a new terminal, activate your environment (if needed):**

```bash
source env/bin/activate
```

#### **3. Run the CLI for a full response:**

```bash
python cli.py "What is the capital of France?"
```

#### **4. Run the CLI for a streaming response:**

```bash
python cli.py "Tell me a joke" --stream
```

- The `--stream` flag will print tokens as they arrive from the `/stream` endpoint.
- Omit `--stream` to use the `/generate` endpoint for a full response.

#### **Example Output**

```bash
$ python cli.py "Tell me a joke" --stream
[Streaming response]
Why did the chicken cross the road? To get to the other side!
```

---

## 📬 API Endpoints

> **Note:** Swagger UI does not display streaming responses in real time. For real-time streaming, use the CLI or Postman.

### `POST /generate`

- **Input:** `{ "prompt": "..." }`
- **Output:** `{ "response": "..." }`
- **Behavior:** Uses Ollama if available, else stub.

### `POST /stream`

- **Input:** `{ "prompt": "..." }`
- **Output:** SSE stream, one token per event
- **Behavior:** Streams tokens from Ollama or stub

---

### Postman

- Import `postman_collection.json`
- Try `/generate` and `/stream`
- **Limitation:** Postman does not support real-time SSE streaming. You will only see the full response after streaming is finished. For real-time streaming, use the CLI or `curl`:
  ```bash
  curl -N -X POST http://127.0.0.1:8000/stream -H "Content-Type: application/json" -d '{"prompt": "Tell me a joke"}'
  ```

### Swagger UI

- Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Note:** Streaming responses will only appear after the stream is finished.

---

## 📜 Logging

- All interactions are logged to `logs/log.jsonl` in JSONL format:
  ```json
  {
    "timestamp": "...",
    "prompt": "...",
    "response": "...",
    "streamed": true,
    "model": "ollama"
  }
  ```

---

## 🔎 Design Choices & Tradeoffs

| Topic                  | Decision                   | Reason                                              |
| ---------------------- | -------------------------- | --------------------------------------------------- |
| Ollama vs Hugging Face | Ollama                     | Fast setup, small disk, production-ready local LLMs |
| Stub Fallback          | Yes                        | Ensures project runs even without Ollama            |
| Streaming              | SSE (not WebSockets)       | Simpler, natively supported, less boilerplate       |
| Split endpoints        | `/generate` and `/stream`  | Clarity, avoids confusion about response type       |
| Web UI                 | Skipped                    | Out of scope; Postman + CLI + Swagger suffice       |
| Token delay simulation | Included in `/stream` stub | Adds realism, mimics LLM latency                    |
| Logging format         | JSONL                      | Efficient for appending, analytics, replay          |

---

## ✅ Submission Checklist

- ✅ Local REST API (stub + optional LLM)
- ✅ Logs all prompts/responses
- ✅ Postman, CLI, Swagger support
- ✅ No internet/cloud dependencies
- ✅ Bonus: streaming token-by-token
