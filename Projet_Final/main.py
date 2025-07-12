import cv2 as cv
import src.get_keyword as get_keyword
import src.get_path as get_path
import src.get_path2 as get_path2
import src.Imagen as Imagen
import src.Poemgen as Poemgen
import src.optimizer as optimizer
import subprocess

# ── CONSTANTS FOR DOBOT AND PATHS ──────────────

# Path to the Python 3.5 executable for the Dobot
PYTHON35_PATH = "C:\\Users\\abde2\\AppData\\Local\\Programs\\Python\\Python35\\python.exe"
DOBOT_DRAWER_PATH = "src/DobotDrawer.py"

# Constants for Image Drawing
IMAGE_PATH = "temp/image.png"

# Constants for Poem Writing
FONT = "Fonts/TT Ricordi Allegria Trial Light.ttf"  # Font for rendering text
FONT_SIZE = 100                  # Font size in points
LINES = 7             # Number of lines for the poem

# ── CONSTANTS FOR DOBOT ARM SETTINGS ───────────

DOBOT_X_MIN = 180  # X-minimum for Dobot (left side)
DOBOT_X_MAX = 300  # X-maximum for Dobot (right side)
DOBOT_Y_MIN = -60  # Y-minimum for Dobot (bottom side)
DOBOT_Y_MAX = 60   # Y-maximum for Dobot (top side)

DOBOT_Z_DRAW = -47 # Z-height for drawing (pen down)
DOBOT_Z_MOVE = -44 # Z-height for moving between paths (pen up)


# ── MAIN FUNCTION ───────────────────────────
def main():
    """
    Listens for a command to either write a poem or draw an image,
    generates the corresponding paths, and sends them to the Dobot.
    """
    cmd = get_keyword.listen()
    if not cmd:
        print("Could not hear a command.")
        return

    keyword = get_keyword.extract_keyword(cmd)
    print(f"Keyword: {keyword}")

    strokes = None
    img_width = 0
    img_height = 0

    # Conditional logic to decide between writing a poem or drawing an image
    if cmd.lower().startswith("write"):
        print("Writing functionality selected.")
        poem = Poemgen.Poemgen(keyword, LINES)
        print("\nGenerated Poem:\n\n" + poem)
        
        print("\nGenerating paths from text...")
        strokes, img_width, img_height = get_path.generate_paths(poem, FONT, FONT_SIZE)

    elif cmd.lower().startswith("draw"):
        print("Drawing functionality selected.")
        Imagen.Imagen(keyword)
        
        print(f"Loading image: {IMAGE_PATH}...")
        original_image = cv.imread(IMAGE_PATH)
        
        if original_image is None:
            print(f"Error: Could not load image at {IMAGE_PATH}")
            return
        else:
            print("Generating outlines...")
            outline_image = get_path2.generate_outline(original_image)
            
            print("Generating paths from outlines...")
            strokes, img_width, img_height = get_path2.generate_paths(outline_image)
    else:
        print("Command not recognized. Please say 'write a poem' or 'draw an image'.")
        return

    # --- Common logic for path optimization and execution ---
    if strokes:
        print(f"Found {len(strokes)} strokes. Optimizing and scaling for Dobot...")
        scaled_strokes = optimizer.scale_strokes_to_dobot(
            strokes, img_width, img_height,
            DOBOT_X_MIN, DOBOT_X_MAX, DOBOT_Y_MIN, DOBOT_Y_MAX
        )
        optimized_strokes = optimizer.optimize_path(scaled_strokes)
        optimizer.save_to_file(optimized_strokes, DOBOT_Z_MOVE, DOBOT_Z_DRAW, DOBOT_X_MIN, DOBOT_X_MAX, DOBOT_Y_MIN, DOBOT_Y_MAX)

        print("Path generated successfully! Sending to Dobot...")
        subprocess.run([PYTHON35_PATH, DOBOT_DRAWER_PATH])
    else:
        print("Could not generate any paths from the input.")


# ── MAIN EXECUTION ───────────────────────────
if __name__ == "__main__":
    main()