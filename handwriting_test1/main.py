import numpy as np
import cv2 as cv
import subprocess
from svgpathtools import svg2paths2
from simplification.cutil import simplify_coords
import optimizer 
import os

# --- Constants ---
OUTPUT_TOOLPATH_FILE = "toolpath.txt"
TOLERANCE = 2  

def remap(value, inputStart, inputEnd, outputStart, outputEnd):
    """Maps a value from one range to another."""
    if (inputEnd - inputStart) == 0:
        return outputStart
    result = (value - inputStart)/(inputEnd - inputStart)*(outputEnd - outputStart) + outputStart
    return result


def generate_paths():
    # svg to path
    paths, attributes, svg_attributes = svg2paths2("samples/force.svg")

    # Find bounds
    all_x = []
    all_y = []
    height = 800 
    width = 800
    aspect_ratio = width / height if height != 0 else 1

    if not paths:
        return [], width, height

    for path in paths:
        min_x_seg, max_x_seg, min_y_seg, max_y_seg = path.bbox()
        all_x.extend([min_x_seg, max_x_seg])
        all_y.extend([min_y_seg, max_y_seg])

    if not all_x or not all_y:
        return [], width, height

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Padding and aspect ratio correction
    if max_x - min_x < max_y - min_y:
        min_y -= height * 0.1
        max_y += height * 0.1
        centre = (max_x + min_x) / 2
        new_width_box = (max_y - min_y) * aspect_ratio
        min_x = centre - new_width_box / 2
        max_x = centre + new_width_box / 2
    else:
        min_x -= width * 0.1
        max_x += width * 0.1
        centre = (max_y + min_y) / 2
        new_height_box = (max_x - min_x) / aspect_ratio
        min_y = centre - new_height_box / 2
        max_y = centre + new_height_box / 2

    all_strokes = []
    density = 20
    for path in paths:
        stroke_points = []
        num_samples = int(path.length() / density * 5) if path.length() is not None else 20
        if num_samples < 2:
            num_samples = 2
        
        points = [path.point(i / float(num_samples - 1)) for i in range(num_samples)]

        for p in points:
            x, y = p.real, p.imag
            new_x = remap(x, min_x, max_x, 0, width)
            new_y = remap(y, min_y, max_y, 0, height)
            stroke_points.append((new_x, new_y))
        all_strokes.append(stroke_points)

    simplified_strokes = [simplify_coords(stroke, TOLERANCE) for stroke in all_strokes]

    # Remove empty strokes and those with only one point

    return simplified_strokes, width, height

# --- Main Execution ---
if __name__ == "__main__":
        print("Generating paths from outlines...")
        strokes, img_width, img_height = generate_paths()
        
        if strokes:
            print(f"Found {len(strokes)} strokes. Optimizing and scaling for Dobot...")
            optimizer.process_and_save(strokes, img_width, img_height, OUTPUT_TOOLPATH_FILE)
            
            print("-" * 20)
            print("Success!")
            print(f"Optimized toolpath saved to: {OUTPUT_TOOLPATH_FILE}")
            print("-" * 20)
        else:
            print("Could not generate any paths from the image.")