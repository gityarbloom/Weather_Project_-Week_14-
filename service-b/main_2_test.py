import requests

def fetch_coordinates(location_name: str):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": location_name,
        "count": 1
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if "results" not in data or not data["results"]:
        raise ValueError(f"Location not found: {location_name}")

    result = data["results"][0]
    return {
        "location_name": result["name"],
        "country": result.get("country"),
        "latitude": result["latitude"],
        "longitude": result["longitude"]
    }

def fetch_hourly_weather(latitude: float, longitude: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,relative_humidity_2m",
        "past_days": 1,
        "timezone": "UTC"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["hourly"]


def ingest_weather_for_location(location_name):
    records = []


    location = fetch_coordinates(location_name)


    hourly_data = fetch_hourly_weather(
        location["latitude"],
        location["longitude"]
    )

    times = hourly_data["time"]
    temperatures = hourly_data["temperature_2m"]
    wind_speeds = hourly_data["wind_speed_10m"]
    humidities = hourly_data["relative_humidity_2m"]


    for i in range(len(times)):
        record = {
            "timestamp": times[i],
            "location_name": location["location_name"],
            "country": location["country"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "temperature": temperatures[i],
            "wind_speed": wind_speeds[i],
            "humidity": humidities[i]

        }
        records.append(record)

    return records





from fastapi import FastAPI, HTTPException
import uvicorn

app1 = FastAPI()


@app1.post("/ingest")
def get_the_data_weather(location_name: str):
    data_weather = ingest_weather_for_location(location_name)

    url = "http://localhost:8001/clean"
    try:
        response = requests.post(url, json=data_weather)
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)


@app1.get("/test")
def test(location_name: str):
    data_weather = ingest_weather_for_location(location_name)
    return data_weather



uvicorn.run(app1, host="localhost", port=8000)
