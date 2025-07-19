import httpx
from typing import Generator, Tuple, Union
import time

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3"
OLLAMA_TIMEOUT = 300  # 5 minutes

# --- Ollama Availability ---
def is_ollama_available() -> bool:
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False

# --- Generate Response ---
def generate_response(prompt: str) -> Tuple[str, str]:
    if is_ollama_available():
        try:
            resp = httpx.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT
            )
            text = resp.text.strip()
            if '\n' in text:
                first_line = text.split('\n', 1)[0]
                data = httpx.Response(200, content=first_line).json()
            else:
                data = resp.json()
            return data.get("response", "[Ollama error: no response]"), "ollama"
        except Exception as e:
            return f"[Ollama error: {e}]", "ollama"
    # Stub fallback
    return f"You said: {prompt}", "stub"

# --- Stream Response (token by token) ---
def stream_response(prompt: str) -> Tuple[Generator[str, None, None], str]:
    if is_ollama_available():
        def ollama_gen():
            try:
                with httpx.stream(
                    "POST",
                    f"{OLLAMA_URL}/api/generate",
                    json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": True},
                    timeout=OLLAMA_TIMEOUT
                ) as resp:
                    for line in resp.iter_lines():
                        if line:
                            try:
                                data = httpx.Response(200, content=line).json()
                                token = data.get("response")
                                if token:
                                    yield token
                            except Exception:
                                continue
            except Exception as e:
                yield f"[Ollama stream error: {e}]"
        return ollama_gen(), "ollama"
    else:
        def stub_gen():
            words = ["You said:"] + prompt.split()
            for i, word in enumerate(words):
                # Add a space before all words except the first
                yield ("" if i == 0 else " ") + word
                time.sleep(0.2)
        return stub_gen(), "stub" 