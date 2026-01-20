import pandas as pd
import numpy as np
from datetime import datetime
import datetime

data = [{'timestamp': datetime.datetime(2026, 1, 19, 0, 0),
  'location_name': 'London',
  'country': 'United Kingdom',
  'latitude': 51.50853,
  'longitude': -0.12574,
  'temperature': -24.7,
  'wind_speed': 3.9,
  'humidity': 83},
 {'timestamp': datetime.datetime(2026, 1, 19, 1, 0),
  'location_name': 'London',
  'country': 'United Kingdom',
  'latitude': 51.50853,
  'longitude': -0.12574,
  'temperature': 18.9,
  'wind_speed': 3.4,
  'humidity': 84},
 {'timestamp': datetime.datetime(2026, 1, 19, 2, 0),
  'location_name': 'London',
  'country': 'United Kingdom',
  'latitude': 51.50853,
  'longitude': -0.12574,
  'temperature': 25.7,
  'wind_speed': 10,
  'humidity': 84},
 {'timestamp': datetime.datetime(2026, 1, 19, 3, 0),
  'location_name': 'London',
  'country': 'United Kingdom',
  'latitude': 51.50853,
  'longitude': -0.12574,
  'temperature': 17.9,
  'wind_speed': 33.87,
  'humidity': 86}]


def dict_to_df(json_data):
    return pd.DataFrame(json_data)


def add_temperature_category(dataframe):
    dataframe["temperature_category"] = pd.cut(x=dataframe["temperature"], bins=[float('-inf'), 18, 25, float('inf')], labels=["cold", "moderate", "hot"], include_lowest=True)
    return dataframe

def add_wind_status(dataframe):
    dataframe["wind_status"] =  dataframe["wind_speed"].apply(lambda x: "windy" if x > 10 else "calm")

def df_to_dict(dataframe):
    return dataframe.to_dict("records")

df = dict_to_df(data)

add_temperature_category(df)

add_wind_status(df)

# print(df.dtypes)

dict_version = df_to_dict(df)

my_dict = dict_version[0]



print(type(data[0]["timestamp"]))


print(type(dict_version[0]["timestamp"]))