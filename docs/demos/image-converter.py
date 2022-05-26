import tosclib as tosc
from PIL import Image
import numpy as np

class ImageConverter():
    def __init__(self, inputFile, outputFile, imagePath, canvasName = "canvas"):
        """ Stores the conversion settings """
        self.input_path = inputFile
        self.output_path = outputFile
        self.image_path = imagePath
        self.image_size = 64
        self.pixel_size = 4
        self.canvas_name = canvasName
        self.pixels = None

    def pixelateImage(self):
        """ Pixelates image and converts it into a numpy array of size (2,3) of x y and rgb."""
        img = Image.open(self.image_path)
        ratio = min(img.size) / self.image_size
        xyr = int(img.size[0] / ratio), int(img.size[1] /ratio)
        imagePixelated = img.resize(xyr, resample=Image.Resampling.BILINEAR)
        self.pixels = np.asarray(imagePixelated)/255

    def drawPixelBoxes(self):
        """ Draws an array of pixels as box objects in a 'canvas' object.
        The canvas is any {self.canvas_name} named object in the top layer.
        """
        root = tosc.load(self.input_path)
        main = tosc.ElementTOSC(root[0])

        canvas = tosc.findChildByName(main.node, self.canvas_name)
        canvas = tosc.ElementTOSC(canvas)
        
        for x in range(int(self.pixels[0].size/3)):
            for y in range(int(self.pixels.size/(self.pixels[0].size))):
                
                box = tosc.ElementTOSC(canvas.createNode("BOX"))

                box.setColor(
                                self.pixels[y][x][0],
                                self.pixels[y][x][1],
                                self.pixels[y][x][2],
                                1
                            )
                box.setFrame(
                                x*self.pixel_size,
                                y*self.pixel_size,
                                self.pixel_size,
                                self.pixel_size
                            )

                box.createProperty("s", "name", f"p{x}{y}")
                box.createProperty("b", "background", "1")

        return tosc.write(root, self.output_path)

def main(inputFile, outputFile, imageFile, target):
    converter = ImageConverter(inputFile, outputFile, imageFile, target)
    converter.image_size = 64
    converter.pixel_size = 4
    converter.pixelateImage()
    converter.drawPixelBoxes()

if __name__ == "__main__":

    main(
            "demos/files/test.tosc",
            "demos/files/out.tosc",
            "demos/files/logo.jpg",
            "canvas"
    )
