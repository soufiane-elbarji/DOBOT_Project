import numpy as np
import cv2 as cv
import random
import img_functions as img
from matplotlib import pyplot as plt
 
# import image
img_origine = cv.imread('samples/darwin.jpg')
img_origine = cv.cvtColor(img_origine, cv.COLOR_BGR2GRAY)
assert img_origine is not None, "file could not be read, check with os.path.exists()"

# generate outline
edges = img.generate_outline(img_origine)

# display result
cv.imshow("outline", edges)
# k = cv.waitKey(0) # Wait for a keystroke in the window
# cv.imwrite('outputs/car_out.jpg', edges_invert)


#########################             FIND STROKES

contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

# Create a 3-channel color image
point_image = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)

# Draw each point
for contour in contours:
    rnd_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    print(str(len(contour)))
    # k = cv.waitKey(0) # Wait for a keystroke in the window
    # cv.imshow("Contour Points", point_image)
    for point in contour:
        x, y = point[0]  # shape is (1, 2)
        cv.circle(point_image, (x, y), radius=1, color=rnd_color, thickness=-1)

cv.putText(point_image, "stroke number : " + str(len(contours)), (10,20), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))
print(str(len(contours)))

# Show the result
cv.imshow("Contour Points", point_image)
cv.destroyAllWindows()

# cv.imwrite('outputs/colored_contours5.jpg', point_image)

#plot image
plt.subplot(1,3,1)
plt.imshow(img_origine, cmap='gray')

#plot contour
plt.subplot(1,3,2)
plt.imshow(edges, cmap='gray')

#plot separated contour
plt.subplot(1,3,3)
plt.imshow(point_image, cmap='gray')

plt.show()
cv.waitKey(0)
