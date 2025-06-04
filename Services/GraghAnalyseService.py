from cProfile import label

import matplotlib
from typing import List
from Models.FileAnanyzerResult import FileAnalysisResult

matplotlib.use('Agg')  # backend ללא GUI
import matplotlib.pyplot as plt
import numpy as np

#Distribution of function lengths
def Histogram(function_lengths: List[int]):
    plt.hist(function_lengths, bins=10, edgecolor='black')
    plt.title("Function Length Distribution")
    plt.xlabel('Length of Functions')
    plt.ylabel('Number of Functions')
    plt.savefig('./GraghsPng/histogram.png')
    plt.close()

#Number of issues per issue type
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
    plt.savefig('./GraghsPng/pie_chart.png')
    plt.close()

#Number of issues per file
def Bar_Chart(list_of_results: List[FileAnalysisResult]):
    filenames  = [file.file_name for file in list_of_results]
    issues = [res.long_functions + res.missing_docstrings + res.unused_vars + (res.total_lines>200) for res in list_of_results ]

    plt.bar(filenames, issues, color='orange')
    plt.title('Total Issues Per File')
    plt.xlabel('File Name')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=90, ha='right')
    plt.tight_layout()
    plt.savefig('./GraghsPng/IssuesBarChart.png')
    plt.close()

#consider implementing a line graph to track the number of issues over time.
def Line_Graph(timed_results: list[tuple[str, int]]):
    """
    timed_results: List of tuples [(timestamp, issue_count)]
    """
    plt.clf()
    timestamps = [t for (t, _) in timed_results]
    issues = [i for (_, i) in timed_results]

    plt.plot(timestamps, issues, marker='o', linestyle='-', color='green')
    plt.title('Issues Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Issues')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('./GraghsPng/IssuesOverTime.png')
    plt.close()




