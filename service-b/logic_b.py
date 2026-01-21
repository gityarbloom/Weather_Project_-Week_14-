import os
import requests
import pandas as pd
from datetime import datetime
from pydantic import BaseModel
from fastapi import HTTPException

class Location(BaseModel):
     timestamp : datetime
     location_name : str
     country : str | None
     latitude : float
     longitude : float
     temperature : float
     wind_speed : float
     humidity : int


def dict_to_df(json_data):
    return pd.DataFrame(json_data)


def add_temperature_category(dataframe):
    dataframe["temperature_category"] = pd.cut(x=dataframe["temperature"], bins=[float('-inf'), 18, 25, float('inf')], labels=["cold", "moderate", "hot"], include_lowest=True)
    return dataframe

def add_wind_status(dataframe):
    dataframe["wind_status"] =  dataframe["wind_speed"].apply(lambda x: "windy" if x > 10 else "calm")
    return dataframe

def df_to_dict(dataframe):
    return dataframe.to_dict("records")

def send_to_service_b(data_weather):
    host_name = os.getenv("SERVICE_C_HOST", "localhost")
    url = f"http://{host_name}:8002/clean"
    try:
        response = requests.post(url, json=data_weather)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=e)