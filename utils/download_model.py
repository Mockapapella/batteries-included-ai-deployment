"""Helper file for downloading models."""

import os

from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

model_repo = "openai-community/gpt2"
local_model_path = "/workspace/models/openai-community/gpt2"
os.makedirs(local_model_path, exist_ok=True)

print(f"Downloading model and tokenizer from {model_repo}...")

try:
    model = AutoModelForCausalLM.from_pretrained(model_repo)
    model.save_pretrained(local_model_path)
    print(f"Model saved to {local_model_path}")

    tokenizer = AutoTokenizer.from_pretrained(model_repo)
    tokenizer.save_pretrained(local_model_path)
    print(f"Tokenizer saved to {local_model_path}")

    print(
        "Download and save complete. You can now use this model and tokenizer in your applications."
    )
except Exception as e:
    print(f"Error downloading the model or tokenizer: {str(e)}")
    exit(1)
