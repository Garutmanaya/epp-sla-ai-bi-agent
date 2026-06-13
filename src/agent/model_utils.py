"""
Handles communication with different model backends via ENV URLs and API Keys.
Each model may have different endpoints and authorization formats.
"""

import os
import requests
import time

# 1. Store URLs
MODEL_URLS = {
    "epp-sla-reporter-model": os.getenv("CUSTOM_MODEL_URL", "http://localhost:8000/predict"),
    "openai": os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions"), # Added standard fallback just in case
    "huggingface": os.getenv("HF_API_URL", "")
}

# 2. Store API Keys / Tokens from Environment Variables
MODEL_KEYS = {
    "epp-sla-reporter-model": os.getenv("CUSTOM_MODEL_API_KEY", ""),
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "huggingface": os.getenv("HF_API_KEY", "")
}

from agent.logger import get_logger
logger = get_logger("api_clients")


def get_headers_for_model(model_name: str) -> dict:
    """
    Generates the appropriate authorization headers based on the model provider.
    """
    api_key = MODEL_KEYS.get(model_name, "")
    headers = {"Content-Type": "application/json"}

    if not api_key:
        return headers

    # Apply the specific authorization format needed for each provider
    if model_name == "openai" or model_name == "huggingface":
        headers["Authorization"] = f"Bearer {api_key}"
    elif model_name == "epp-sla-reporter-model":
        # Adjust 'x-api-key' to match whatever header your custom model server/API Gateway expects
        headers["x-api-key"] = api_key

    return headers


def get_model_predictions(model_name: str, question: str):

    url = MODEL_URLS.get(model_name)
    logger.info(f"[{model_name}] Preparing request")

    if not url:
        logger.error(f"[{model_name}] Missing URL")
        return {
            "sql": "",
            "raw": None,
            "latency": None,
            "error": f"Missing ENV for {model_name}"
        }

    # Dynamically fetch the authorization headers
    headers = get_headers_for_model(model_name)
    payload = {"question": question}

    logger.info(f"[{model_name}] POST → {url}")
    logger.debug(f"[{model_name}] Payload: {payload}")

    start = time.time()

    try:
        # Pass the headers dictionary into the requests.post call
        response = requests.post(url, json=payload, headers=headers, timeout=60)

        logger.info(f"[{model_name}] Status Code: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        logger.info(f"[{model_name}] SQL Generated")

        return {
            "sql": data.get("sql", ""),
            "raw": data,
            "latency": time.time() - start,
            "error": None
        }

    except Exception as e:
        logger.exception(f"[{model_name}] API Call Failed")
        return {
            "sql": "",
            "raw": None,
            "latency": None,
            "error": str(e)
        }
