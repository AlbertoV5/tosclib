from src import toscEdit
from src import gui
from pathlib import Path

from tosclib import tosc

tosc = toscEdit.Design(directory="")

src = Path.cwd() / "src" / "image-tosc"
inputPath = src / "input"
outputPath = src / "output"

tosc.loadFiles(
    input_path = inputPath / "input", 
    output_path = outputPath / "output", 
    image_path = inputPath /"bg", 
    pixel_path = inputPath / "pixel")

tosc.image_size = 64
tosc.pixel_size = 8

gui.start(tosc)
