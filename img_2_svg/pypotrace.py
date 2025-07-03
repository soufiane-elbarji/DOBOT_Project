from PIL import Image
import subprocess

# Convert BMP to PBM
img = "darwing_edge.bmp"
potrace = "img_to_stroke_meth1\potrace-1.16.win64\potrace"

# Run potrace to get SVG
subprocess.run([potrace, img, "-s", "-o", "darwing_edge.svg"])
