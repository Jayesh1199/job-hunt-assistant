import os
from dotenv import load_dotenv

# Load .env for local development
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)

# Read keys — works both locally (.env) and on Streamlit Cloud (secrets)
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "").strip()
USAJOBS_EMAIL = os.getenv("USAJOBS_EMAIL", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
