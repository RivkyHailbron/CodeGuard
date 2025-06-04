import ast
import json
from Models.FileAnalysistResult import FileAnalysisResult


def save_analysis(result: FileAnalysisResult):
        try:
            with open("analysis_log.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(result.to_dict())

        with open("analysis_log.json", "w") as f:
            json.dump(data, f, indent=2)



def analyze_file(file_name, code):
    tree = ast.parse(code)
    lines = code.splitlines()
    total_lines = len(lines)

    function_lengths = []
    missing_docstrings = 0
    unused_vars = set()
    used_vars = set()
    assigned_vars = set()

    class Analyzer(ast.NodeVisitor):
        def __init__(self):
            self.scopes = []  # Stack of scopes

        def push_scope(self):
            self.scopes.append({'assigned': set(), 'used': set()})

        def pop_scope(self):
            scope = self.scopes.pop()
            unused = scope['assigned'] - scope['used']
            return unused

        def current_scope(self):
            return self.scopes[-1] if self.scopes else None

        def visit_FunctionDef(self, node):
            print(f"funcName {node.name}")
            nonlocal missing_docstrings
            self.push_scope()

            # Function length
            start_line = node.lineno
            end_line = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start_line)
            function_lengths.append(end_line - start_line + 1)

            # Missing docstring
            if not ast.get_docstring(node):
                missing_docstrings += 1

            self.generic_visit(node)

            # Analyze unused variables in this function
            unused_vars_in_func = self.pop_scope()
            unused_vars.update(unused_vars_in_func)

        def visit_Name(self, node):
            scope = self.current_scope()
            if scope:
                if isinstance(node.ctx, ast.Store):
                    scope['assigned'].add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    scope['used'].add(node.id)
            else:
                if isinstance(node.ctx, ast.Store):
                    assigned_vars.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    used_vars.add(node.id)
            self.generic_visit(node)

    Analyzer().visit(tree)

    # unused global variables
    unused_vars.update(assigned_vars - used_vars)

    long_functions = sum(1 for l in function_lengths if l > 20)

    return FileAnalysisResult(
        file_name=file_name,
        total_lines=total_lines,
        num_functions=len(function_lengths),
        function_lengths=function_lengths,
        long_functions=long_functions,
        unused_vars=len(unused_vars),
        missing_docstrings=missing_docstrings
    )

def save_analysis(result: FileAnalysisResult):
    try:
        with open("analysis_log.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(result.to_dict())

    with open("analysis_log.json", "w") as f:
        json.dump(data, f, indent=2)

def  combined_results(results:list[FileAnalysisResult]):
    combined = {
        "function_lengths": [],
        "total_lines": 0,
        "long_functions": 0,
        "missing_docstrings": 0,
        "unused_vars": 0
    }
    for result in results:
        combined["function_lengths"].extend(result.function_lengths)
        combined["total_lines"] += result.total_lines
        combined["long_functions"] += result.long_functions
        combined["missing_docstrings"] += result.missing_docstrings
        combined["unused_vars"] += result.unused_vars

    return combined