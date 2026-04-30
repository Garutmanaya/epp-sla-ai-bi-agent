
"""
Handles communication with different model backends via ENV URLs.
Each model may have different endpoints.
"""

import os
import requests
import time

MODEL_URLS = {
    "epp-sla-reporter-model": os.getenv("CUSTOM_MODEL_URL", "http://localhost:8000/predict"),
    "openai": os.getenv("OPENAI_API_URL", ""),
    "huggingface": os.getenv("HF_API_URL", "")
}

from agent.logger import get_logger
logger = get_logger("api_clients") 

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

    payload = {"question": question}

    logger.info(f"[{model_name}] POST → {url}")
    logger.debug(f"[{model_name}] Payload: {payload}")

    start = time.time()

    try:
        response = requests.post(url, json=payload, timeout=60)

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



