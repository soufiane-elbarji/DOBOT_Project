from PIL import Image
import subprocess

# Convert BMP to PBM
img = "outputs\image_4.bmp"
potrace = "potrace-1.16.win64\potrace"

# Run potrace to get SVG
subprocess.run([potrace, img, "-s", "-o", "imqge_4.svg"])
