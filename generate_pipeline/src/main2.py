import numpy as np
import cv2 as cv
import random
import img_functions as img_func
from svgpathtools import svg2paths, svg2paths2
from matplotlib import pyplot as plt
from PIL import Image
import subprocess

 
# import image
img_origine = cv.imread('samples/image_3.png')
assert img_origine is not None, "file could not be read, check with os.path.exists()"

# gray :P
img_gray = cv.cvtColor(img_origine, cv.COLOR_BGR2GRAY)

# generate outline
edges = img_func.generate_outline(img_origine)
edges_invert = cv.bitwise_not(edges)

cv.imwrite('pipeline/4/edge.bmp', edges_invert)

## outline to SVG


# Convert BMP to PBM
img = "pipeline/4/edge.bmp"
potrace = "../potrace-1.16.win64/potrace"

# Run potrace to get SVG
subprocess.run([potrace, img, "-s", "-o", "pipeline/4/svg_outline.svg"])


# svg to path
paths, attributes, svg_attributes  = svg2paths2("pipeline/4/svg_outline.svg")
print(str(len(paths)))
print(svg_attributes)

# Find bounds
all_x = []
all_y = []
height, width = edges.shape[:2]
aspect_ratio = width / height

for path in paths:
    for seg in path:
        min_x, max_x, min_y, max_y = seg.bbox()
        all_x.append(min_x)
        all_x.append(max_x)
        all_y.append(min_y)
        all_y.append(max_y)

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)

if max_x - min_x < max_y - min_y:
    min_y -= height*0.1
    max_y += height*0.1
    centre = (max_x + min_x)/2
    new_width = (max_y - min_y) * aspect_ratio
    min_x = centre - new_width/2
    max_x = centre + new_width/2
else:
    min_x -= width*0.1
    max_x += width*0.1
    centre = (max_y + min_y)/2
    new_width = (max_x - min_x) * aspect_ratio
    min_y = centre - new_width/2
    max_y = centre + new_width/2

print (f"{min_x}, {max_x}")
print (f"{min_y}, {max_y}")


point_image_svg = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
density = 10
# Flatten into points
for path in paths:
    rnd_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    for segment in path:
        for t in [i/density for i in range(density+1)]:  # Sample the path
            point = segment.point(t)
            x, y = point.real, point.imag
            # print(f"x : {x} , y : {y}")
            new_x = int(img_func.remap(x, min_x, max_x, 0, width))
            new_y = int(img_func.remap(y, min_y, max_y, 0, height))
            cv.circle(point_image_svg, (new_x, new_y), radius=1, color=rnd_color, thickness=-1)
            # Now x, y is one coordinate the robot should go to

point_image_svg = cv.flip(point_image_svg, 0)
cv.imshow("svg paths", point_image_svg)

cv.imwrite('pipeline/4/paths.jpg', point_image_svg)

# generate svg form outline (bitmape tarcing)


# # plot image
# plt.subplot(1,3,1)
# plt.imshow(img_origine)

# #plot contour
# plt.subplot(1,3,2)
# plt.imshow(edges_invert, cmap='gray')

# # plot contours (colored)
# plt.subplot(1,3,3)
# plt.imshow(point_image)

# plt.show()
cv.waitKey(0)









# generate contours
# contours, _ = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)


# ### display contours
# # Create a 3-channel color image
# point_image = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)

# # Draw each point
# for contour in contours:
#     rnd_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#     # print(str(len(contour)))
#     # k = cv.waitKey(0) # Wait for a keystroke in the window
#     # cv.imshow("Contour Points", point_image)
#     for point in contour:
#         x, y = point[0]  # shape is (1, 2)
#         cv.circle(point_image, (x, y), radius=1, color=rnd_color, thickness=-1)
# cv.putText(point_image, "stroke number : " + str(len(contours)), (10,20), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
# print("stroke number :" + str(len(contours)))
