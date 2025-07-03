import numpy as np
import cv2 as cv
import random
import img_functions as img_func
from svgpathtools import svg2paths, svg2paths2
from matplotlib import pyplot as plt
from PIL import Image
import subprocess
from simplification.cutil import simplify_coords

 
# import image
img_origine = cv.imread('samples/darwin.jpg')
assert img_origine is not None, "file could not be read, check with os.path.exists()"

# gray :P
img_gray = cv.cvtColor(img_origine, cv.COLOR_BGR2GRAY)

# generate outline
edges = img_func.generate_outline(img_origine)

paths = img_func.generate_paths(edges)
print(paths)

# ### PLOTING PATHS COMPARISON

plt.figure(figsize=(6, 6))
plt.title("Simplified Stroke Points")

for path in paths:
    x_vals = [p[0] for p in path]
    y_vals = [p[1] for p in path]
    plt.plot(x_vals, y_vals)  # s = point size

plt.gca().set_aspect('equal')
plt.grid(True)
plt.show()
