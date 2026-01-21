import pymysql
from fastapi import FastAPI
import uvicorn


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

    def create_locations_db(self, db_name):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.conn.select_db(db_name)
        self.conn.commit()
        self.db = db_name

    def create_locations_table(self, table_name):
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



    def select_all(self):
        self.mysqlconnect()
        cur = self.conn.cursor()
        cur.execute("select * from locations_table")
        output = cur.fetchall()

        for i in output:
            print(i)

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    db_conn = MySQLConnection("localhost", "root", "")
    db_conn.mysqlconnect()
    db_conn.create_locations_db("locations_db")
    db_conn.create_locations_table("locations_table")
    db_conn.select_all()
    db_conn.close_connection()






