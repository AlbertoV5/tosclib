from src import toscEdit
from src import gui
import subprocess
from pathlib import Path

tosc = toscEdit.Design(directory="")

cwd = Path.cwd()
input = cwd / "input"
out = cwd / "output"

tosc.loadFiles(
    input_path = input / "input", 
    output_path = out / "output", 
    image_path = input /"bg", 
    pixel_path = input / "pixel")

tosc.image_size = 64
tosc.pixel_size = 8

gui.start(tosc)

#subprocess.run(f"start {tosc.output_path}.tosc", shell=True, check=True)
#os.system(f"start {out}.tosc")