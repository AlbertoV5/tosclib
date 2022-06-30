import tosclib as tosc
from PIL import Image  # type: ignore
import numpy as np
import time

from tosclib.elements import ControlType


class ImageConverter:
    def __init__(self, inputFile, outputFile, imagePath, canvasName="canvas"):
        """Stores the conversion settings"""
        self.input_path = inputFile
        self.output_path = outputFile
        self.image_path = imagePath
        self.image_size = 64
        self.pixel_size = 4
        self.canvas_name = canvasName
        self.pixels = None

    def pixelateImage(self):
        """Pixelates image and converts it into a numpy array of size (h,w,3)"""
        img = Image.open(self.image_path)
        ratio = min(img.size) / self.image_size
        xyr = int(img.size[0] / ratio), int(img.size[1] / ratio)
        imagePixelated = img.resize(xyr, resample=Image.Resampling.BILINEAR)
        self.pixels = np.asarray(imagePixelated) / 255

    def drawPixelBoxes(self):
        """Draws an array of pixels as box objects in a 'canvas' object.
        The canvas is any {self.canvas_name} named object in the top layer.
        """
        root = tosc.load(self.input_path)
        main = tosc.Node(root[0])
        canvas = tosc.find_child(main.node, self.canvas_name)
        ecanvas = tosc.Node(canvas)

        pxs = self.pixel_size
        for iy, ix in np.ndindex(self.pixels.shape[:2]):
            (r, g, b) = self.pixels[iy, ix]
            box = tosc.Box(
                name=f"p{ix}{iy}",
                color=(r, g, b, 1),
                frame=(ix * pxs, iy * pxs, pxs, pxs),
            )
            ecanvas.children.append(tosc.xml_control(box))

        return tosc.write(root, self.output_path)


def main(inputFile, outputFile, imageFile, target):
    converter = ImageConverter(inputFile, outputFile, imageFile, target)
    converter.image_size = 64
    converter.pixel_size = 4
    converter.pixelateImage()
    converter.drawPixelBoxes()


if __name__ == "__main__":
    start = time.process_time()
    main(
        "docs/demos/files/test.tosc",
        "docs/demos/files/out.tosc",
        "docs/demos/files/logo.jpg",
        "canvas",
    )
    end = time.process_time()
    print("Converter", end - start)
