import subprocess

def potrace(img_path, output_svg_path):
    
    turdsize_val = 1
    opttolerance_val = 0.0
    alphamax_val = 1
    turnpolicy_val = "minority"


    command = [
        "potrace",
        img_path,
        "-s", 
        "-o", output_svg_path,
        "-t", str(turdsize_val),
        "-O", str(opttolerance_val),
        "-a", str(alphamax_val),
        "-z", turnpolicy_val,
    ]

    subprocess.run(command)