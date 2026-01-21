from fastapi import FastAPI, HTTPException
from logic import *
import os
import uvicorn

app = FastAPI()

@app.post("/ingest")
def get_the_data_weather(location_name: str):
    data_weather = ingest_weather_for_location(location_name)

    host_name = os.getenv("SERVICE_B_HOST", "localhost")
    url = f"http://{host_name}:8001/clean"
    # url = f"http://localhost:8001/clean"
    try:
        response = requests.post(url, json=data_weather)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)