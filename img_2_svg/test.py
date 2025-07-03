import subprocess

img_path = "image_5.bmp"
output_svg_path = "image_5-1.svg"
potrace_executable = "img_to_stroke_meth1\\potrace-1.16.win64\\potrace"

turdsize_val = 1
opttolerance_val = 0.0
alphamax_val = 1
turnpolicy_val = "minority"


command = [
    potrace_executable,
    img_path,
    "-s", 
    "-o", output_svg_path,
    "-t", str(turdsize_val),
    "-O", str(opttolerance_val),
    "-a", str(alphamax_val),
    "-z", turnpolicy_val,
]

subprocess.run(command)
print(f"SVG file generated: {output_svg_path}")