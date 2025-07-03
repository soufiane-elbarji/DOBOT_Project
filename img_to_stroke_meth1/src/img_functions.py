import numpy as np
import cv2 as cv
import subprocess
from svgpathtools import svg2paths, svg2paths2
from simplification.cutil import simplify_coords


POTRACE_PATH = "../potrace-1.16.win64/potrace"
tolerance = 2  # Higher = more aggressive simplification (in pixels or mm)


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
    img_blur = cv.GaussianBlur(img_resize, (5, 5), 0) 
    # img_blur = cv.medianBlur(img_resize, 3)

    # EDGE DETECTION
    edges = cv.Canny(img_resize,100,200)
    return edges

def generate_paths(edges):
    edges_invert = cv.bitwise_not(edges)

    cv.imwrite('temp/edge.bmp', edges_invert)

    # Convert BMP to PBM
    img = "temp/edge.bmp"
    potrace = POTRACE_PATH

    # Run potrace to get SVG
    subprocess.run([potrace, img, "-s", "-o", "temp/svg_outline.svg"])


    # svg to path
    paths, attributes, svg_attributes  = svg2paths2("temp/svg_outline.svg")

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
        min_y -= height*0.2
        max_y += height*0.2
        centre = (max_x + min_x)/2
        new_width = (max_y - min_y) * aspect_ratio
        min_x = centre - new_width/2
        max_x = centre + new_width/2
    else:
        min_x -= width*0.2
        max_x += width*0.2
        centre = (max_y + min_y)/2
        new_height = (max_x - min_x) * aspect_ratio
        min_y = centre - new_height/2
        max_y = centre + new_height/2


    all_strokes = []  
    density = 20 
    # Flatten into points
    for path in paths:
        stroke_points = []
        for segment in path:
            for t in [i/density for i in range(density-1)]:  # Sample the path
                point = segment.point(t)
                x, y = point.real, point.imag
                # print(f"x : {x} , y : {y}")
                new_x = int(remap(x, min_x, max_x, 0, width))
                new_y = int(remap(y, min_y, max_y, 0, height))

                stroke_points.append((new_x, new_y))
        all_strokes.append(stroke_points)

    simplified_strokes = []

    for stroke in all_strokes:
        # RDP requires a flat list of [x, y] pairs
        simplified = simplify_coords(stroke, tolerance)
        simplified_strokes.append(simplified)

    return simplified_strokes