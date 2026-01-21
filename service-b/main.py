from fastapi import FastAPI
from logic_b import *
import uvicorn

app = FastAPI()

@app.post("/clean")
def clean_data(data:list[Location]):
    dict_version = [l.model_dump(mode='json') for l in data]
    df = dict_to_df(dict_version)
    df = add_temperature_category(df)
    df = add_wind_status(df)
    data_weather = df_to_dict(df)
    data_weather = send_to_service_b(data_weather)

    return data_weather

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)