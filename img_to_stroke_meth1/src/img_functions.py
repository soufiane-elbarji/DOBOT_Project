import numpy as np
import cv2 as cv

# includes resizing + blur(needs tweaking for non cartoon imgs) before canny 
def generate_outline(img):
    # downscale image
    original_height, original_width = img.shape[:2]

    new_width = 800
    aspect_ratio = new_width / original_width
    new_height = int(original_height * aspect_ratio)  # Compute height based on aspect ratio 
    img_resize = cv.resize(img, (new_width, new_height))

    # BLUR
    img_blur = cv.GaussianBlur(img_resize, (5, 5), 0) 

    # EDGE DETECTION
    edges = cv.Canny(img_blur,100,200)
    edges_invert = cv.bitwise_not(edges)
    return edges

#
# def generate_contours(outline):
#     contours, _ = cv.findContours(outline, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
