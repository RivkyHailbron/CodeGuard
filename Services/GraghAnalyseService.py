import os
from cProfile import label
from datetime import datetime

import matplotlib
from typing import List
from Models.FileAnanyzerResult import FileAnalysisResult

matplotlib.use('Agg')  # backend ללא GUI
import matplotlib.pyplot as plt


# Distribution of function lengths
def Histogram(function_lengths: List[int]):
    filename = f'./GraghsPng/histogram.png'
    plt.hist(function_lengths, bins=10, edgecolor='black')
    plt.title("Function Length Distribution")
    plt.xlabel('Length of Functions')
    plt.ylabel('Number of Functions')
    plt.savefig(filename)
    plt.close()

# Number of issues per issue type
def Pie_Chart(results: dict, num_files: int):
    filename = f'./GraghsPng/pie_chart.png'
    file_size_issues = results["total_lines"] // 200
    parts = [
        file_size_issues,
        results["long_functions"],
        results["missing_docstrings"],
        results["unused_vars"]
    ]
    labels = ["Total Lines > 200", "Long Functions", "Missing Docstrings", "Unused Variables"]
    plt.pie(parts, labels=labels, autopct='%1.1f%%')
    plt.title(f"Code Issues Across {num_files} Files")
    plt.savefig(filename)
    plt.close()

# Number of issues per file
def Bar_Chart(list_of_results: List[FileAnalysisResult]):
    filename = f'./GraghsPng/IssuesBarChart.png'
    filenames = [file.file_name for file in list_of_results]
    issues = [res.long_functions + res.missing_docstrings + res.unused_vars + (res.total_lines > 200) for res in list_of_results]

    plt.bar(filenames, issues, color='orange')
    plt.title('Total Issues Per File')
    plt.xlabel('File Name')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

# Consider implementing a line graph to track the number of issues over time
def Line_Graph(results: list[FileAnalysisResult]):
    filename = f'./GraghsPng/line_graph.png'
    timed_data = []
    for res in results:
        total_issues = res.long_functions + res.unused_vars + res.missing_docstrings + (res.total_lines > 200)
        time = datetime.fromisoformat(res.timestamp)
        timed_data.append((time, total_issues))

    timed_data.sort(key=lambda x: x[0])
    times = [t.strftime("%Y-%m-%d %H:%M") for t, _ in timed_data]
    issues = [i for _, i in timed_data]

    plt.clf()
    plt.figure(figsize=(10, 5))
    plt.plot(times, issues, marker='o', linestyle='-', color='green')
    plt.title('Issues Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
def delete_old_images(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)