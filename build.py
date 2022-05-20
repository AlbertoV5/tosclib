from pathlib import Path
import subprocess

def execute(cmd):

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

# docs_path = Path("docs") / Path("make")
# execute(f"{docs_path} html")
# execute("")

"""
cd tosclib

python -m build

pip install dist/tosclib-0.1-py3-none-any.whl

cd ../

docs\make html



"""