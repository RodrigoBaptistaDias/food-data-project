import requests
from dotenv import load_dotenv
import os
import json
from google.cloud import storage, secretmanager
from fastapi import HTTPException
from datetime import datetime

load_dotenv()

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.getenv("GCP_PROJECT_ID")
    version_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(name=version_path)
    secret_value = response.payload.data.decode("UTF-8")
    return secret_value


def storing_json_in_gcs(url,payload,headers):
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        storage_client = storage.Client()
        bucket_name = os.getenv("GCS_BUCKET_TRANSIENT")
        bucket = storage_client.bucket(bucket_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"dublin_restaurants_data{timestamp}.json"
        blob = bucket.blob(file_name)
        
        compressed_data = json.dumps(data).encode('utf-8')
        blob.upload_from_string(compressed_data, content_type='application/json')
        
        success_message = f"file {file_name} succesfully saved in bucket {bucket_name}"
        print(success_message)
        return {"status": "success", "message":success_message}
    
    except Exception as e:
        error_message =f"Unspected erro: {e}" 
        print(error_message)
        raise HTTPException(status_code=500, detail=error_message)
    