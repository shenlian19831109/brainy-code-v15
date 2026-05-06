import subprocess
import tempfile
import os

class LSPValidator:
    def validate(self, code: str, filename: str = "generated.py") -> bool:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        try:
            if filename.endswith('.py'):
                result = subprocess.run(['python', '-m', 'py_compile', temp_path],
                                        capture_output=True)
            elif filename.endswith(('.ts', '.tsx', '.js', '.jsx')):
                result = subprocess.run(['npx', 'tsc', '--noEmit', temp_path],
                                        capture_output=True)
            else:
                return True
            return result.returncode == 0
        except:
            return False
        finally:
            os.unlink(temp_path)