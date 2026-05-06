import os
import re
import ast

class MinimalIR:
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.symbols = []

    def build(self):
        self.symbols = []
        for dirpath, _, filenames in os.walk(self.project_root):
            for fname in filenames:
                if fname.endswith('.py'):
                    self._extract_python(os.path.join(dirpath, fname))
                elif fname.endswith(('.ts', '.tsx', '.js', '.jsx')):
                    self._extract_typescript(os.path.join(dirpath, fname))

    def _extract_python(self, filepath):
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self.symbols.append({
                        'name': node.name,
                        'params': len(node.args.args),
                        'file': os.path.relpath(filepath, self.project_root)
                    })
        except:
            pass

    def _extract_typescript(self, filepath):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            pattern1 = re.findall(r'function\s+(\w+)\s*\(', content)
            pattern2 = re.findall(r'(?:const|let|var)\s+(\w+)\s*=\s*\(.*?\)\s*=>', content)
            for name in pattern1 + pattern2:
                self.symbols.append({
                    'name': name,
                    'params': -1,
                    'file': os.path.relpath(filepath, self.project_root)
                })
        except:
            pass

    def get_function_names(self) -> list:
        return list(set(s['name'] for s in self.symbols))

    def exists(self, func_name: str) -> bool:
        return any(s['name'] == func_name for s in self.symbols)