import numpy as np
import cv2 as cv
import random
import img_functions as img
from svgpathtools import svg2paths, svg2paths2
from matplotlib import pyplot as plt
 
# import image
img_origine = cv.imread('samples/image_4.png')
assert img_origine is not None, "file could not be read, check with os.path.exists()"

# gray :P
img_gray = cv.cvtColor(img_origine, cv.COLOR_BGR2GRAY)

# generate outline
edges = img.generate_outline(img_origine)
edges_invert = cv.bitwise_not(edges)

cv.imwrite('outputs/image_4.bmp', edges_invert)

# svg to path
paths, attributes, svg_attributes  = svg2paths2("imqge_4.svg")
print(str(len(paths)))
print(svg_attributes)

# Find bounds
all_x = []
all_y = []

for path in paths:
    min_x, max_x, min_y, max_y = path.bbox()
    all_x.append(min_x)
    all_x.append(max_x)
    all_y.append(min_y)
    all_y.append(max_y)

min_x, max_x = min(all_x), max(all_x)
min_y, max_y = min(all_y), max(all_y)
min_coord = min(min_x, min_y)
max_coord = max(max_x, max_y)

print (f"{min_x}, {max_x}")
print (f"{min_y}, {max_y}")


point_image_svg = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
density = 20
# Flatten into points
for path in paths:
    rnd_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    for segment in path:
        for t in [i/density for i in range(density+1)]:  # Sample the path
            point = segment.point(t)
            x, y = point.real, point.imag
            # print(f"x : {x} , y : {y}")
            scale = 1.6
            new_x, new_y = int(img.remap(x, 0, scale*max_coord , 0, 1200)), int(img.remap(y, 0, scale*max_coord, 0, 1200))
            cv.circle(point_image_svg, (new_x, new_y), radius=1, color=rnd_color, thickness=-1)
            # Now x, y is one coordinate the robot should go to

point_image_svg = cv.flip(point_image_svg, 0)
cv.imshow("svg paths", point_image_svg)

# cv.imwrite('outputs/teapot2_strokes_color.jpg', point_image_svg)

# generate svg form outline (bitmape tarcing)


# plot image
plt.subplot(1,3,1)
plt.imshow(img_origine)

#plot contour
plt.subplot(1,3,2)
plt.imshow(edges_invert, cmap='gray')

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
