from http.client import HTTPException
from typing import List
from fastapi.staticfiles import StaticFiles

import uvicorn
from fastapi import FastAPI, UploadFile,File
from fastapi.responses import FileResponse ,JSONResponse,HTMLResponse
from pydantic import BaseModel

from Services.AnalyseService import analyze_file, save_analysis, combine_results, load_results_from_json
from Services.GraghAnalyseService import Histogram, Pie_Chart, Bar_Chart, Line_Graph

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
        result = analyze_file(file.filename , data.decode("utf-8"))
        save_analysis(result)
        results.append(result)

    combine= combine_results(results)
    Histogram(combine["function_lengths"])
    Pie_Chart(combine , len(files))
    Bar_Chart(results)
    Line_Graph(load_results_from_json())

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
        <head>
            <style>
                html, body {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    overflow: hidden;
                }
                h1 {
                    color: #333;
                    margin: 10px 0;
                    text-align: center;
                }
                .grid-container {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    grid-template-rows: 1fr 1fr;
                    height: calc(100vh - 60px);
                    gap: 10px;
                    padding: 10px;
                    box-sizing: border-box;
                }
                .graph-item {
                    position: relative;
                    overflow: hidden;
                    border-radius: 12px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    background: white;
                }
                .graph-item img {
                    width: 100%;
                    height: 100%;
                    object-fit: contain;
                    display: block;
                }
                .download-btn {
                    position: absolute;
                    bottom: 10px;
                    right: 10px;
                    background-color: rgba(76, 175, 80, 0.9);
                    color: white;
                    padding: 6px 12px;
                    border-radius: 6px;
                    font-size: 14px;
                    text-decoration: none;
                    transition: background-color 0.3s ease;
                }
                .download-btn:hover {
                    background-color: rgba(56, 142, 60, 0.95);
                }

                @media (max-width: 768px) {
                    .grid-container {
                        grid-template-columns: 1fr;
                        grid-template-rows: repeat(4, 1fr);
                    }
                }
            </style>
        </head>
        <body>
            <h1>All Graphs</h1>
            <div class="grid-container">
                <div class="graph-item">
                    <img src="/GraghsPng/histogram.png" alt="Histogram">
                    <a href="/GraghsPng/histogram.png" download class="download-btn">הורד</a>
                </div>
                <div class="graph-item">
                    <img src="/GraghsPng/pie_chart.png" alt="Pie Chart">
                    <a href="/GraghsPng/pie_chart.png" download class="download-btn">הורד</a>
                </div>
                <div class="graph-item">
                    <img src="/GraghsPng/IssuesBarChart.png" alt="Bar Chart">
                    <a href="/GraghsPng/IssuesBarChart.png" download class="download-btn">הורד</a>
                </div>
                <div class="graph-item">
                    <img src="/GraghsPng/line_graph.png" alt="Line Graph">
                    <a href="/GraghsPng/line_graph.png" download class="download-btn">הורד</a>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content