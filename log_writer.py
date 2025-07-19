import os
import json
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "log.jsonl")

def log_interaction(prompt: str, response: str, streamed: bool, model: str = None) -> None:
    """
    Appends a prompt/response pair with timestamp and metadata to logs/log.jsonl in JSONL format.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "prompt": prompt,
        "response": response,
        "streamed": streamed,
        "model": model or "unknown"
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n") 