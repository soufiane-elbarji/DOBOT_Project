from PIL import Image, ImageDraw, ImageFont
import subprocess

potrace = "C:\\Users\\pc\\Documents\\GitHub\\DOBOT_Project\\potrace-1.16.win64\\potrace.exe"

# --- Configuration ---

text_to_render = "\n".join([
    "This is the first line of the paragraph.",
    "This is the second line.",
    "And this is the third."
])

font_file = "Fonts/EduNSWACTCursive-Regular.ttf"
font_size = 60
output_file = "img.bmp"
final_svg = "img.svg"

# --- Create the Image ---
img = Image.new('RGB', (1200, 1200), color='white')
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype(font_file, font_size)
except IOError:
    print(f"Font file '{font_file}' not found. Using default font.")

center_x = img.width / 2
center_y = img.height / 2

# Draw the multi-line text block, centered as a whole
draw.text(
    (center_x, center_y),
    text_to_render,
    font=font,
    fill='black',
    anchor="mm"  # This correctly centers the entire text block
)

img.save(output_file)
print(f"Successfully created '{output_file}' with paragraph text.")

# Convert the BMP image to SVG using potrace
subprocess.run([potrace, output_file, '-o', final_svg, '--svg'])
print(f"Successfully converted to '{final_svg}'.")