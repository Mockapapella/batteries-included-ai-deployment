"""Helper file for downloading models."""

import os

from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer

# Define the local path to save the model and tokenizer
local_model_path = "/workspace/models/twitter-xlm-roberta-base-sentiment-finetunned"

# Ensure the directory exists
os.makedirs(local_model_path, exist_ok=True)

# Download and save the model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(
    "citizenlab/twitter-xlm-roberta-base-sentiment-finetunned"
)
tokenizer = AutoTokenizer.from_pretrained(
    "citizenlab/twitter-xlm-roberta-base-sentiment-finetunned"
)
model.save_pretrained(local_model_path)
tokenizer.save_pretrained(local_model_path)
