from tosclib import tosc, gui
from PIL import Image
import numpy as np
import argparse

class ImageConverter():
    def __init__(self, inputFile, outputFile, imagePath, canvasName = "canvas"):
        """ Stores the conversion data and functions for the GUI to point to
        """
        self.input_path = inputFile
        self.output_path = outputFile
        self.image_path = imagePath
        self.image_size = 64
        self.pixel_size = 4
        self.canvas_name = canvasName
        self.image_pixelated = None
        self.pixels = None

    def pixelateImage(self):
        """ Pixelates image and converts it into a numpy array
        of size (2,3) of x y and rgb.
        """
        img = Image.open(self.image_path)
        ratio = min(img.size) / self.image_size

        xyr = int(img.size[0] / ratio), int(img.size[1] /ratio)
        imagePixelated = img.resize(xyr, resample=Image.Resampling.BILINEAR)

        self.pixels = np.asarray(imagePixelated)/255

        xyr = xyr[0]*self.pixel_size, xyr[1]*self.pixel_size
        self.image_pixelated = img.resize(xyr, resample=Image.Resampling.NEAREST)


    def drawPixelBoxes(self):
        """ Draws an array of pixels as box objects in a 'canvas' object.
        The canvas is any {self.canvas_name} named object in the top layer.
        """
        root = tosc.load(self.input_path)
        main = tosc.ElementTOSC(root[0])

        canvas = tosc.findChildByName(main.node, self.canvas_name)
        canvas = tosc.ElementTOSC(canvas)

        # TO DO: Add ET.remove() for all elements inside canvas first!

        for x in range(int(self.pixels[0].size/3)):
            for y in range(int(self.pixels.size/(self.pixels[0].size))):
                
                box = tosc.ElementTOSC(canvas.createNode("BOX"))

                box.createProperty("c", "color", "", {
                                    "r" : str(self.pixels[y][x][0]),
                                    "g" : str(self.pixels[y][x][1]),
                                    "b" : str(self.pixels[y][x][2]),
                                    "a" : "1"
                                })
                box.createProperty("r", "frame", "", {
                                    "x" : str(x*self.pixel_size), 
                                    "y" : str(y*self.pixel_size), 
                                    "w" : str(self.pixel_size), 
                                    "h" : str(self.pixel_size)
                                })
                box.createProperty("s", "name", f"p{x}{y}")
                box.createProperty("b", "background", "1")

        return tosc.write(root, self.output_path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = ".tosc file", required=True)
    parser.add_argument("-o", "--Output", help = ".tosc file", required=True)
    parser.add_argument("-j", "--Image", help = ".jpg file")
    parser.add_argument("-t", "--Target", help = "Name of the Touch OSC object in top layer")

    args = parser.parse_args()
    
    #For testing purposes
    args.Image = "tests/logo.jpg" if args.Image == None else args.Image
    args.Target = "canvas" if args.Target == None else args.Target

    converter = ImageConverter(args.Input, args.Output, args.Image, args.Target)
    converter.image_size = 64
    converter.pixel_size = 4

    gui.start(converter)
