import os
import requests
from utils.config import USAJOBS_API_KEY

def fetch_usajobs(keyword, location="remote", results_per_page=5):
    headers = {
        "Authorization-Key": USAJOBS_API_KEY,
        "User-Agent": os.getenv("USAJOBS_EMAIL"),
        "Host": "data.usajobs.gov"
    }

    params = {
        "Keyword": keyword,
        "LocationName": location,
        "ResultsPerPage": results_per_page
    }

    url = "https://data.usajobs.gov/api/search"

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["SearchResult"]["SearchResultItems"]
    else:
        print(f"Error: {response.status_code}")
        return []