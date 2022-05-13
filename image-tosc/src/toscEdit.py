from PIL import Image
import numpy as np
import xml.etree.ElementTree as ET
from uuid import uuid4
from pathlib import Path

class Design():
    def __init__(self, directory):
        self.cwd = Path.cwd() / directory

    def loadFiles(self, input_path, output_path, image_path, pixel_path):
        self.input_path = self.cwd / input_path
        self.output_path = self.cwd / output_path
        self.image_path = self.cwd / image_path
        self.pixel_path = self.cwd / pixel_path
        self.tree = ET.parse(f"{self.input_path}.xml")
        self.root = self.tree.getroot()
        self.seed = ET.parse(f"{self.pixel_path}.xml")
        self.target = self.root.findall("node")[0].find("children").find("node").find("children")
        self.image_size = 64
        self.pixel_size = 4

    def pixelateImage(self):
        img = Image.open(f"{self.image_path}.jpg")
        ratio = min(img.size) / self.image_size
        xyr = int(img.size[0] / ratio), int(img.size[1] /ratio)
        self.image_pixelated = img.resize(xyr, resample=Image.Resampling.BILINEAR)
        self.pixels = np.asarray(self.image_pixelated)/255
        xyr = xyr[0]*self.pixel_size, xyr[1]*self.pixel_size
        self.image_pixelated = img.resize(xyr, resample=Image.Resampling.NEAREST)

    def drawBox(self, colorTargets, frameTargets, name):
        with open(f"{self.pixel_path}.xml", "r") as file:
            seed = ET.fromstring(file.read())
        seed.attrib["ID"] = str((uuid4()))
        for values in seed:
            for val in values:
                if val.find("key").text == "color":
                    for color in colorTargets:
                        val.find("value").find(color).text = str(colorTargets[color])
                if val.find("key").text == "frame":
                    for frame in frameTargets:
                        val.find("value").find(frame).text = str(frameTargets[frame])
                if val.find("key").text == "name":
                    val.find("value").text = name
    
        self.target.append(seed)

    def draw(self):
        for x in range(int(self.pixels[0].size/3)):
            for y in range(int(self.pixels.size/(self.pixels[0].size))):
                colorTargets = {"r":self.pixels[y][x][0], "g":self.pixels[y][x][1], "b":self.pixels[y][x][2]}
                frameTargets = {"x":x*self.pixel_size, "y":y*self.pixel_size, "w":self.pixel_size, "h":self.pixel_size}   
                self.drawBox(colorTargets, frameTargets, "p"+str(x)+str(y))

    def save(self):
        self.tree.write(f"{self.output_path}.xml")
        self.tree.write(f"{self.output_path}.tosc")
        print(f"Saved to {self.output_path}")

