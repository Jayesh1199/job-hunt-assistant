import os
from dotenv import load_dotenv

# Get the directory where this config.py file lives (utils/)
utils_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(utils_dir, ".env")

load_dotenv(dotenv_path, override=True)

USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "").strip()
USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()