

from http.client import HTTPException
from typing import List
from fastapi.staticfiles import StaticFiles

import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel

from Services.AnalyseService import analyze_file, save_analysis, combine_results
from Services.GraghAnalyseService import Histogram, Pie_Chart, Bar_Chart


app = FastAPI()
app.mount("/GraghsPng", StaticFiles(directory="GraghsPng"), name="graphs")

@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post("/analyze")
async def analyze(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        data = await file.read()
        result = analyze_file(file.filename, data.decode("utf-8"))
        save_analysis(result)
        results.append(result)

    combine = combine_results(results)
    Histogram(combine["function_lengths"])
    Pie_Chart(combine, len(files))
    Bar_Chart(results)

    return JSONResponse(content={
        "message": "Analysis completed",
        "view_graphs_url": "/show_graphs"
    })


@app.post("/alerts")
async def alerts(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        data = await file.read()
        result = analyze_file(file.filename, data.decode("utf-8"))
        results.append(result)
    return JSONResponse(combine_results(results))


@app.get("/show_graphs", response_class=HTMLResponse)
async def show_graphs():
    html_content = """
    <html>
        <body>
            <h1>Graphs</h1>
            <img src="/GraghsPng/histogram.png" alt="Histogram" width="600"/><br/>
            <img src="/GraghsPng/pie_chart.png" alt="Pie Chart" width="600"/><br/>
            <img src="/GraghsPng/IssuesBarChart.png" alt="Line Graph" width="600"/>
        </body>
       <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                text-align: center;
                padding: 30px;
                margin: 0;
            }
            h1 {
                color: #333;
                margin-bottom: 40px;
            }
            .graphs-container {
                display: flex;
                justify-content: center;
                gap: 20px;
                flex-wrap: nowrap; /* לא מאפשר גלילה אופקית */
                overflow-x: hidden;
            }
            .graph-item {
                flex: 1 1 20%; /* כל תמונה תתאים עד כ-20% רוחב */
                max-width: 22%; /* גודל מקסימלי לתמונה */
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .graph-item img {
                width: 100%;
                height: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                border-radius: 10px;
                user-select: none;
            }
            .download-btn {
                margin-top: 10px;
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
                transition: background-color 0.3s ease;
            }
            .download-btn:hover {
                background-color: #45a049;
            }
        
            /* למובייל: מציג 2 גרפים בשורה */
            @media (max-width: 800px) {
                .graphs-container {
                    flex-wrap: wrap;
                }
                .graph-item {
                    max-width: 45%;
                    margin-bottom: 20px;
                }
            }
            /* למובייל קטן: גרף אחד בשורה */
            @media (max-width: 450px) {
                .graph-item {
                    max-width: 90%;
                }
            }
    </style>

    </html>
    """
    return html_content

