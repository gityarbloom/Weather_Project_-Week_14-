import pymysql
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from datetime import datetime


app3 = FastAPI()

class Location(BaseModel):
    timestamp: datetime
    location_name: str
    country: str | None
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float
    humidity: int
    temperature_category : str
    wind_status : str



class MySQLConnection:
    def __init__(self, host, root, password):
        self.host = host
        self.root = root
        self.password = password
        self.conn = None
        self.db = None
        self.table = None


    def mysqlconnect(self):
        if self.conn is None:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.root,
                password=self.password
            )

    def create_db(self, db_name):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.conn.select_db(db_name)
        self.conn.commit()
        self.db = db_name

    def create_table(self, table_name):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            timestamp DATETIME,
            location_name VARCHAR(50),
            country VARCHAR(50),
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            wind_speed FLOAT,
            humidity INT,
            temperature_category VARCHAR(50) NOT NULL,
            wind_category VARCHAR(50) NOT NULL
        )
        """)
        self.conn.commit()
        self.table = table_name

    def insert_into(self, timestamp, location_name, country, latitude, longitude, temperature, wind_speed, humidity, temperature_category, wind_category):
        self.mysqlconnect()
        cur = self.conn.cursor()
        sql_query = f"""
        INSERT INTO {self.table} (timestamp, location_name, country, latitude, longitude, temperature, wind_speed, humidity, temperature_category, wind_category)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (timestamp, location_name, country, latitude, longitude,temperature, wind_speed, humidity, temperature_category, wind_category)
        cur.execute(sql_query, values)
        self.conn.commit()



    def select_all(self):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"select * from {self.table}")
        output = cur.fetchall()
        return output


    def close_connection(self):
        self.conn.close()
        self.conn = None



@app3.post("/test_connection_to_database")
def test_db(data: list[Location]):
    dict_version = [l.model_dump(mode='json') for l in data]
    db_conn = MySQLConnection("localhost", "root", "")
    db_conn.create_db("project_db")
    db_conn.create_table("records_weather)")
    for loc in dict_version:
        db_conn.insert_into(loc["timestamp"], loc["location_name"], loc["country"], loc["latitude"], loc["longitude"], loc["temperature"], loc["wind_speed"], loc["humidity"], loc["temperature_category"], loc["wind_status"])
    results = db_conn.select_all()
    db_conn.close_connection()
    return {"message" : "Successful"}

if __name__ == "__main__":
    uvicorn.run(app3, host="localhost", port=8002)






