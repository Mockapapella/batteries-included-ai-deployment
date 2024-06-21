"""FastAPI server to perform AI text generation with GPT-2."""

import logging

import torch
from fastapi import FastAPI
from fastapi import HTTPException
from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer
from transformers import pipeline

from utils.config import APP_NAME
from utils.config import OTLP_GRPC_ENDPOINT
from utils.logging import logger
from utils.logging import setup_logging
from utils.middleware import PrometheusMiddleware
from utils.utils import metrics
from utils.utils import setup_otlp

setup_logging(logging.INFO)

# Setting up model pipeline
local_model_path = "/workspace/models/openai-community/gpt2"
model = GPT2LMHeadModel.from_pretrained(local_model_path)
tokenizer = GPT2Tokenizer.from_pretrained(local_model_path)
device = 0 if torch.cuda.is_available() else -1
text_generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setup_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


@app.get("/generate/")
def generate_text(prompt: str, max_length: int = 50):
    """Generate text based on an incoming prompt."""
    logger.info(f"Received prompt: {prompt}")
    if not prompt:
        raise HTTPException(status_code=400, detail="No prompt provided for text generation.")
    try:
        result = text_generator(prompt, max_length=max_length, num_return_sequences=1)
        generated_text = result[0]["generated_text"]
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
