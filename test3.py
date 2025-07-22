import numpy as np
from autotrace import Bitmap, VectorFormat
from PIL import Image

image_path = "img.png"
pil_image = Image.open(image_path).convert("RGB")

image_array = np.asarray(pil_image)

bitmap = Bitmap(image_array)

vector = bitmap.trace(
    centerline=True,
)

output_svg_path = "output.svg"
vector.save(output_svg_path)

svg_bytes = vector.encode(VectorFormat.SVG)

print(f"Image successfully traced with centerline, saved as {output_svg_path}!")