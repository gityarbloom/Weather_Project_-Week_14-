import pandas as pd
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

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


@app.post("/clean")
def clean_data(data:list[Location]):
    dict_version = [l.model_dump(mode='json') for l in data]
    df = dict_to_df(dict_version)
    df = add_temperature_category(df)
    df = add_wind_status(df)
    final_dict = df_to_dict(df)
    return final_dict

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)