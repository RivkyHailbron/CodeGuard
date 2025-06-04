from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse

from Models.FileAnalysistResult import FileAnalysisResult
from Services.AnalysisService import analyze_file, save_analysis,combined_results
from Services.grap_analyze_service import Histogram, Pie_Chart

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post('/analyze')
async def analyze(files: List[UploadFile] = File(...)):

     results:list[FileAnalysisResult]= []
     for file in files:
         content = await file.read()
         result = analyze_file(file.fileName,content.decode("utf-8"))
         results.append(result)
         save_analysis(result)

    combined_results = combined_results(results)
    Histogram(combined_results["function_lengths"])
    Pie_Chart(combined_results, len(files))
    histogram_path = './graphs_png/histogram.png'
    pie_chart_path = './graphs_png/pie_chart.png'


    # Return JSON response with links to the graphs
    return JSONResponse(content={
     "message": "Analysis completed",
     "graphs": {
            "histogram": histogram_path,
            "pie_chart": pie_chart_path
     }
    })


@app.post('/alerts')
async def create_alert(alert_data: dict):

    return JSONResponse(content={"message": "Alert created", "data": alert_data})