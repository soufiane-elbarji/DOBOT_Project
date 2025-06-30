import numpy as np
import cv2 as cv

def remap(value, inputStart, inputEnd, outputStart, outputEnd):
    result = (value - inputStart)/(inputEnd - inputStart)*(outputEnd - outputStart) + outputStart
    return result

# includes resizing + blur(needs tweaking for non cartoon imgs) before canny 
def generate_outline(img):
    # downscale image
    original_height, original_width = img.shape[:2]

    new_width = 800
    aspect_ratio = new_width / original_width
    new_height = int(original_height * aspect_ratio)  # Compute height based on aspect ratio 
    img_resize = cv.resize(img, (new_width, new_height))

    # BLUR
    img_blur = cv.GaussianBlur(img_resize, (3, 3), 0) 
    # img_blur = cv.medianBlur(img_resize, 3)

    # EDGE DETECTION
    edges = cv.Canny(img_resize,100,200)
    return edges

#
# def generate_contours(outline):
#     contours, _ = cv.findContours(outline, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
