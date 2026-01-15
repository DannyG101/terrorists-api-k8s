from fastapi import FastAPI, UploadFile
import pandas as pd
from pydantic import BaseModel
import pymongo
import os


MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")

my_client = pymongo.MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
my_db = my_client[MONGO_DB]
my_col = my_db["top_threats"]

app = FastAPI()

class Terrorist(BaseModel):
    name : str
    location : str
    danger_rate : int


@app.post("/top-threats")
def read_file(file: UploadFile):
    if not file.filename.lower().endswith(('.csv', ".xlsx", ".xls")):
        return {"error:400": "Invalid CSV file."}
    terr_dict = {}
    top = []
    df = pd.read_csv(file.file)
    df.sort_values("danger_rate", ascending=False)
    df = df.head(5)
    df = df.to_dict(orient='records')
    terr_dict["count"] = len(df)
    for terrorist in df:
        cur_terrorist = Terrorist(name=terrorist["name"], location= terrorist["location"], danger_rate=terrorist["danger_rate"])
        dict_version = cur_terrorist.model_dump()
        top.append(dict_version)
    terr_dict["top"] = top
    x = my_col.insert_one(terr_dict)
    terr_dict.pop("_id")
    return terr_dict