import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

# Fixed import for running from project root
from backend.src.models.predict import main as predict_main

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BAKU_TZ = timezone(timedelta(hours=4))

app = FastAPI(
    title="FastAPI Backend server for chatbot project",
    description="REST API for ML project",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "baku_time": datetime.now(BAKU_TZ).isoformat(),
    }

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "")

    def response_generator():
        for chunk in predict_main(user_input):
            yield chunk

    return StreamingResponse(response_generator(), media_type="text/plain")
