from PIL import Image
import subprocess

# Convert BMP to PBM
img = "image_5.bmp"
potrace = "img_to_stroke_meth1\potrace-1.16.win64\potrace"

# Run potrace to get SVG
subprocess.run([potrace, img, "-s", "-o", "imqge_5.svg"])
