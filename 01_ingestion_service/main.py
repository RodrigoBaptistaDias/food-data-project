from dotenv import load_dotenv
from fastapi import FastAPI
from logic import get_secret, storing_json_in_gcs

load_dotenv()

app = FastAPI()

@app.get("/")
def run_ingestion():

    api_key = get_secret("food-data-project-api-key")
    api_host = get_secret("food-data-project-api-host")


    url = f"https://{api_host}/api/job"

    payload = {
        "scraper": {
            "query": "pizza",
            "address": "Dublin, Ireland",
            "page": 1,
            "maxRows": 80,
            "locale": "en-IE"
        }
    }

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host,
        "Content-Type": "application/json"
    }
    return (storing_json_in_gcs(url,payload,headers))
    
    