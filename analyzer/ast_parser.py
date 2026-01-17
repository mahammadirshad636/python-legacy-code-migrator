import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.classes = []
        self.functions = []
        self.imports = []
        self.complex_functions = []

    def visit_ClassDef(self, node):
        self.classes.append({
            "name": node.name,
            "line": node.lineno,
            "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)])
        })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        args = len(node.args.args)
        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "args": args
        })
        if args > 6:
            self.complex_functions.append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node):
        for n in node.names:
            self.imports.append(n.name)

    def visit_ImportFrom(self, node):
        self.imports.append(node.module)
