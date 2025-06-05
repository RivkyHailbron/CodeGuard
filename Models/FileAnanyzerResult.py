from datetime import datetime

class FileAnalysisResult:

    def __init__(self, file_name, total_lines, num_functions, function_lengths,
                 long_functions, unused_vars, missing_docstrings, timestamp=None):
        self.file_name = file_name
        self.total_lines = total_lines
        self.num_functions = num_functions
        self.function_lengths = function_lengths
        self.long_functions = long_functions
        self.unused_vars = unused_vars
        self.missing_docstrings = missing_docstrings
        self.timestamp = timestamp or datetime.now().isoformat()  # תוספת

    def to_dict(self):
        return self.__dict__
