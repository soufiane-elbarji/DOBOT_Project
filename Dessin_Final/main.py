import cv2 as cv
import src.get_keyword as get_keyword
import src.get_path as get_path
import src.Imagen as Imagen
import src.optimizer as optimizer
import subprocess

# ── CONSTANTS FOR DOBOT SETTINGS ──────────────

IMAGE_PATH = "temp/image.png"

# Adjust the path to your Python 3.5 executable
PYTHON35_PATH = "C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python35\\python.exe"

DOBOT_DRAWER_PATH = "src/DobotDrawer.py"

DOBOT_X_MIN = 200 # X-minimum for Dobot (left side)
DOBOT_X_MAX = 300 # X-maximum for Dobot (right side)
DOBOT_Y_MIN = -50  # Y-minimum for Dobot (bottom side)
DOBOT_Y_MAX = 50   # Y-maximum for Dobot (top side)

DOBOT_Z_DRAW = -55 # Z-height for drawing (pen down)
DOBOT_Z_MOVE = -45  # Z-height for moving between paths (pen up)


# ── MAIN FUNCTION ───────────────────────────
def main():
    cmd = get_keyword.listen()
    if not cmd:
        return

    keyword = get_keyword.extract_keyword(cmd)
    print("Keyword:", keyword)

    Imagen.Imagen(keyword)

    print(f"Loading image: {IMAGE_PATH}...")
    original_image = cv.imread(IMAGE_PATH)
    
    if original_image is None:
        print(f"Error: Could not load image at {IMAGE_PATH}")
    else:
        print("Generating outlines...")
        outline_image = get_path.generate_outline(original_image)
        
        print("Generating paths from outlines...")
        strokes, img_width, img_height = get_path.generate_paths(outline_image)
        
        if strokes:
            print(f"Found {len(strokes)} strokes. Optimizing and scaling for Dobot...")
            scaled_strokes = optimizer.scale_strokes_to_dobot(strokes, img_width, img_height, DOBOT_X_MIN, DOBOT_X_MAX, DOBOT_Y_MIN, DOBOT_Y_MAX)
            optimized_strokes = optimizer.optimize_path(scaled_strokes)
            optimizer.save_to_file(optimized_strokes, DOBOT_Z_MOVE, DOBOT_Z_DRAW)

            print("Path generated successfully!")
        else:
            print("Could not generate any paths from the image.")

    subprocess.run([PYTHON35_PATH, DOBOT_DRAWER_PATH])


# ── MAIN EXECUTION ───────────────────────────
if __name__ == "__main__":
    main()