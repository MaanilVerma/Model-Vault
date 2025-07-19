from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Generator

from model_handler import generate_response, stream_response
from log_writer import log_interaction

app = FastAPI(title="MiniVault API", description="Local prompt/response engine with Ollama or stub fallback.")

class PromptRequest(BaseModel):
    prompt: str = Field(
        ..., 
        example="What is the best thing about apples?",
        description="The prompt or question to send to the model."
    )

@app.post("/generate")
def generate_endpoint(req: PromptRequest):
    try:
        response, model = generate_response(req.prompt)
        if response.startswith("[Ollama error:"):
            raise HTTPException(status_code=503, detail=response)
        log_interaction(req.prompt, response, streamed=False, model=model)
        return {"response": response}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream")
def stream_endpoint(req: PromptRequest):
    token_gen, model = stream_response(req.prompt)
    try:
        first_token = next(token_gen)
    except StopIteration:
        first_token = None
    except Exception as e:
        def error_stream():
            yield f"data: ERROR: {str(e)}\n\n"
        return StreamingResponse(error_stream(), media_type="text/event-stream", status_code=500)

    if first_token and first_token.startswith("[Ollama stream error:"):
        def error_stream():
            yield f"data: ERROR: {first_token}\n\n"
        # Log nothing for error
        return StreamingResponse(error_stream(), media_type="text/event-stream", status_code=503)

    def event_stream_and_log():
        tokens = []
        if first_token:
            tokens.append(first_token)
            yield f"data: {first_token}\n\n"
        for token in token_gen:
            tokens.append(token)
            yield f"data: {token}\n\n"
        # After streaming, log the full response (ignoring error tokens)
        log_interaction(req.prompt, "".join([t for t in tokens if t and not t.startswith("[Ollama stream error:")]), streamed=True, model=model)

    return StreamingResponse(event_stream_and_log(), media_type="text/event-stream", status_code=200) 