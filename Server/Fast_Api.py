from http.client import HTTPException
import uvicorn
from fastapi import FastAPI, UploadFile,File
from fastapi.responses import FileResponse ,JSONResponse
from pydantic import BaseModel

from Services.AnalyseService import analyze_file, save_analysis

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    print("in analyze")
    data = await file.read();
    print("after read")
    print(data)
    print("_________________________________________")
    result = analyze_file(file.filename , data.decode("utf-8"))
    print(f"result {result}")
    save_analysis(result)
    return result




#@app.post("/alerts")
#async





