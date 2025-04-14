import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.2")
ORGANIZATION_ID = os.getenv("ORGANIZATION_ID")  # Optional organization ID
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

# Validate required environment variables
if not HF_API_TOKEN:
    raise ValueError("HF_API_TOKEN environment variable is not set. Please set it in a .env file.")

# Optional warning for Stability API key
if not STABILITY_API_KEY:
    print("Warning: STABILITY_API_KEY is not set. Image generation will not be available.") 