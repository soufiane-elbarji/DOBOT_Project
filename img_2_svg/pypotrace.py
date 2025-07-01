from PIL import Image
import subprocess

# Convert BMP to PBM
img = "img_to_stroke_meth1\\outputs\\teapot2_edge.bmp"
potrace = "img_to_stroke_meth1\\potrace-1.16.win64\\potrace"

# Run potrace to get SVG
subprocess.run([potrace, img, "-s", "-o", "output.svg"])
