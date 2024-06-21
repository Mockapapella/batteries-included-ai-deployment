"""FastAPI server to perform AI predictions."""

import logging

import torch
from fastapi import FastAPI
from fastapi import HTTPException
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
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
local_model_path = "/workspace/models/twitter-xlm-roberta-base-sentiment-finetunned"
model = AutoModelForSequenceClassification.from_pretrained(local_model_path)
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
device = 0 if torch.cuda.is_available() else -1
sentiment_classifier = pipeline(
    "text-classification", model=model, tokenizer=tokenizer, device=device
)

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name=APP_NAME)
app.add_route("/metrics", metrics)

# Setting OpenTelemetry exporter
setup_otlp(app, APP_NAME, OTLP_GRPC_ENDPOINT)


@app.get("/predict/")
def analyze_sentiment(message: str):
    """Return a sentiment score for a request."""
    logger.info(f"Recieved message: {message}")
    if not message:
        raise HTTPException(status_code=400, detail="No message provided for analysis.")
    try:
        result = sentiment_classifier(message)
        return {"label": result[0]["label"], "score": result[0]["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
