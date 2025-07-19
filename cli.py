import argparse
import httpx
import sys

CLI_TIMEOUT = 300  # 5 minutes

def main():
    parser = argparse.ArgumentParser(description="MiniVault CLI: Send a prompt to the local API.")
    parser.add_argument("prompt", type=str, help="Prompt to send")
    parser.add_argument("--stream", action="store_true", help="Stream response token-by-token")
    args = parser.parse_args()

    if args.stream:
        try:
            with httpx.stream(
                "POST",
                "http://127.0.0.1:8000/stream",
                json={"prompt": args.prompt},
                timeout=CLI_TIMEOUT
            ) as resp:
                if resp.status_code != 200:
                    print(f"[Error: {resp.status_code} {resp.reason_phrase}]")
                    sys.exit(1)
                print("[Streaming response]")
                for line in resp.iter_lines():
                    if line:
                        if isinstance(line, bytes):
                            line = line.decode("utf-8")
                        if line.startswith("data:"):
                            token = line[5:].strip()
                            print(token, end=" ", flush=True)
                print()
        except Exception as e:
            print(f"[Error streaming from API: {e}]")
    else:
        try:
            print("[Waiting for response...]")
            resp = httpx.post("http://127.0.0.1:8000/generate", json={"prompt": args.prompt}, timeout=CLI_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            print(data.get("response", "[No response]"))
        except Exception as e:
            print(f"[Error contacting API: {e}]")

if __name__ == "__main__":
    main() 