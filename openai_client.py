import os
import httpx
from dotenv import load_dotenv   # <- add
from openai import OpenAI

# Load .env and override anything already in the environment
load_dotenv(override=True)

_client = None

def get_client():
    global _client
    if _client:
        return _client

    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()

    # TEMP DEBUG — see what Flask is actually using
    print(">>> OPENAI_API_KEY prefix:", api_key[:10], "len:", len(api_key))

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    proxy = os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    http_client = httpx.Client(proxy=proxy, timeout=60) if proxy else httpx.Client(timeout=60)

    # If you *must* use a project-scoped key, you can also pass project explicitly:
    project = os.getenv("OPENAI_PROJECT")  # optional
    _client = OpenAI(api_key=api_key, http_client=http_client, project=project) if project \
              else OpenAI(api_key=api_key, http_client=http_client)

    return _client
