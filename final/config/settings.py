import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
ORS_API_KEY = os.getenv("ORS_API_KEY")
# DB_URL = "postgresql://postgres:Hana%402407@10.10.1.61:5432/AI TP"