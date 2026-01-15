from fastapi import FastAPI, UploadFile
import pandas as pd
import uvicorn

app = FastAPI()


@app.post("/top-threats")
def read_file(file: UploadFile):
    df = pd.read_csv(file.file)
    return len(df)

uvicorn.run(app)