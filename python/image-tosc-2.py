from tosclib import tosc
from PIL import Image
import numpy as np

def ImageToTOSC(inputFile, outputFile, imageFile):

    image_size = 64
    pixel_size = 4

    # Pillow
    img = Image.open(f"{imageFile}")
    ratio = min(img.size) / image_size
    xyr = int(img.size[0] / ratio), int(img.size[1] /ratio)
    image_pixelated = img.resize(xyr, resample=Image.Resampling.BILINEAR)

    # Numpy    
    pixels = np.asarray(image_pixelated)/255

    gui_xyr = xyr*pixel_size
    gui_image_pixelated = img.resize(xyr, resample=Image.Resampling.NEAREST)

    # TOSC
    root = tosc.load(inputFile)
    main = tosc.Node.getMainElements(root[0])

    canvas = tosc.Node.findChildByName(main["node"], "canvas")
    canvas = tosc.Node.getMainElements(canvas)

    for x in range(int(pixels[0].size/3)):
        for y in range(int(pixels.size/(pixels[0].size))):
            tosc.Util.createBox(
                                    canvas["node"], 
                                    {
                                        "r" : str(pixels[y][x][0]),
                                        "g" : str(pixels[y][x][1]),
                                        "b" : str(pixels[y][x][2]),
                                        "a" : str(1)
                                    }, 
                                    {
                                        "x" : str(x*pixel_size), 
                                        "y" : str(y*pixel_size), 
                                        "w" : str(pixel_size), 
                                        "h" : str(pixel_size)
                                    }, 
                                    "p"+str(x)+str(y)
                                )

    tosc.write(root, outputFile)


if __name__ == "__main__":
    ImageToTOSC("test.tosc", "out.tosc", "logo.jpg")