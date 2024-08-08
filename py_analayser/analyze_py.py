import ast
import os 

class PythonFileAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = None
        self.results = ""

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            file_content = file.read()
            self.tree = ast.parse(file_content)

    def analyze(self):
        if not self.tree:
            self.parse_file()

        functions = [node for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(self.tree) if isinstance(node, ast.ClassDef)]
        imports = [node for node in ast.walk(self.tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)]

        self.results += f"Number of functions: {len(functions)}\n"
        self.results += f"Number of classes: {len(classes)}\n"
        self.results += "Imports:\n"
        for imp in imports:
            if isinstance(imp, ast.Import):
                self.results += f"  - {', '.join(alias.name for alias in imp.names)}\n"
            elif isinstance(imp, ast.ImportFrom):
                self.results += f"  - from {imp.module} import {', '.join(alias.name for alias in imp.names)}\n"

        self.results += "\nFunction Details:\n"
        for func in functions:
            func_name = func.name
            args = [arg.arg for arg in func.args.args]
            docstring = ast.get_docstring(func) or "No docstring"
            start_line = func.lineno
            end_line = func.end_lineno if hasattr(func, 'end_lineno') else "Unknown"
            self.results += (f"  Function name: {func_name}\n"
                             f"    Arguments: {args}\n"
                             f"    Docstring: {docstring}\n"
                             f"    Start line: {start_line}\n"
                             f"    End line: {end_line}\n")

        self.results += "\nClass Details:\n"
        for cls in classes:
            cls_name = cls.name
            docstring = ast.get_docstring(cls) or "No docstring"
            start_line = cls.lineno
            end_line = cls.end_lineno if hasattr(cls, 'end_lineno') else "Unknown"
            self.results += (f"  Class name: {cls_name}\n"
                             f"    Docstring: {docstring}\n"
                             f"    Start line: {start_line}\n"
                             f"    End line: {end_line}\n")

    def save_results_to_file(self, output_directory):
        # Create the directory if it does not exist
        os.makedirs(output_directory, exist_ok=True)

        # Define the full path to the output file
        output_path = os.path.join(output_directory, 'analysis_results.txt')

        # Write the results to the file
        with open(output_path, 'w') as file:
            file.write(self.results)

if __name__ == "__main__":
    analyzer = PythonFileAnalyzer(r'path/to/the/file')
    analyzer.analyze()
    analyzer.save_results_to_file('analysis_results.txt')