import ast
import re

class ConstraintExecutor:
    def __init__(self, ir: MinimalIR):
        self.ir = ir
        self.max_retries = 3

    def validate(self, code: str) -> tuple[bool, list[str]]:
        called = self._extract_calls(code)
        violations = []
        for func in called:
            if not self.ir.exists(func) and not self._is_common_builtin(func):
                violations.append(func)
        return len(violations) == 0, violations

    def _extract_calls(self, code: str) -> set:
        calls = set()
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        calls.add(node.func.attr)
        except:
            calls = set(re.findall(r'(\w+)\s*\(', code))
        return calls

    def _is_common_builtin(self, name: str) -> bool:
        builtins = {'print','len','range','int','str','float','list','dict','set','tuple',
                    'open','input','isinstance','getattr','setattr','type','True','False','None',
                    'Exception','super','self','cls',
                    'require','console','log','document','window','fetch',
                    'setTimeout','setInterval','JSON','Math','Promise',
                    'useState','useEffect','useRef','useContext',
                    }
        return name in builtins or name.startswith('__')