from typing import List

import matplotlib.pyplot as plt

from Models.FileAnalysistResult import FileAnalysisResult
import numpy as np
matplotlib.use('Agg')

def Histogram(function_lengths: List[int]):
    plt.hist(function_lengths, bins=10, color='blue', edgecolor='black')
    plt.title("Function Length Distribution")
    plt.xlabel('Length of Functions')
    plt.ylabel('Number of Functions')
    plt.savefig('./graphs_png/histogram.png')
    plt.close()

def Pie_Chart(results: dict, num_files: int):
    file_size_issues = results["total_lines"] // 200  # חישוב כמה קבצים עברו את מגבלת השורות
    parts = [
        file_size_issues,
        results["long_functions"],
        results["missing_docstrings"],
        results["unused_vars"]
    ]
    labels = ["Total Lines > 200", "Long Functions", "Missing Docstrings", "Unused Variables"]
    plt.pie(parts, labels=labels, autopct='%1.1f%%')
    plt.title(f"Code Issues Across {num_files} Files")
    plt.savefig('./graphs_png/pie_chart.png')
    plt.close()
def	Bar_Chart(list_of_result:List[FileAnalysisResult]):
        files_name=[file.file_name for file in list_of_result]
        values = [for ]


