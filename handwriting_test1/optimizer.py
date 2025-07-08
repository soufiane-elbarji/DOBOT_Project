import numpy as np

# --- DOBOT PHYSICAL WORKSPACE CONFIGURATION ---
# This defines the 100x100mm drawing area in front of the Dobot
# Adjust these values to match your physical setup
DOBOT_X_MIN = 200
DOBOT_X_MAX = 300
DOBOT_Y_MIN = -50
DOBOT_Y_MAX = 50

# Z-axis heights for drawing and moving
DOBOT_Z_DRAW = -62 # Z-height for drawing (pen down)
DOBOT_Z_MOVE = -50  # Z-height for moving between paths (pen up)

def remap(value, inputStart, inputEnd, outputStart, outputEnd):
    """Maps a value from one range to another."""
    return (value - inputStart)/(inputEnd - inputStart)*(outputEnd - outputStart) + outputStart

def scale_strokes_to_dobot(strokes, img_width, img_height):
    """Scales the pixel coordinates to the Dobot's physical mm coordinates."""
    scaled_strokes = []
    # Preserve aspect ratio
    img_aspect = img_width / img_height
    dobot_aspect = (DOBOT_X_MAX - DOBOT_X_MIN) / (DOBOT_Y_MAX - DOBOT_Y_MIN)
    
    if img_aspect > dobot_aspect:
        # Image is wider, scale based on X axis
        scale_factor = (DOBOT_X_MAX - DOBOT_X_MIN) / img_width
    else:
        # Image is taller, scale based on Y axis
        scale_factor = (DOBOT_Y_MAX - DOBOT_Y_MIN) / img_height
        
    new_w = img_width * scale_factor
    new_h = img_height * scale_factor
    
    x_offset = DOBOT_X_MIN + ((DOBOT_X_MAX - DOBOT_X_MIN) - new_w) / 2
    y_offset = DOBOT_Y_MIN + ((DOBOT_Y_MAX - DOBOT_Y_MIN) - new_h) / 2

    for stroke in strokes:
        scaled_stroke = []
        for x, y in stroke:
            # Remap from image pixel space to Dobot mm space
            dobot_x = x_offset + (x * scale_factor)
            dobot_y = y_offset + (y * scale_factor)
            scaled_stroke.append((dobot_x, dobot_y))
        scaled_strokes.append(scaled_stroke)
    return scaled_strokes

def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def optimize_path(strokes):
    """
    Sorts strokes using the 'Line Flipping' algorithm to find an efficient path.
    """
    if not strokes:
        return []

    # Copy the list to avoid modifying the original
    remaining_strokes = list(strokes)
    optimized_path = [remaining_strokes.pop(0)]
    
    current_point = optimized_path[0][-1]

    while remaining_strokes:
        min_dist = float('inf')
        best_stroke_index = -1
        reverse_stroke = False

        for i, stroke in enumerate(remaining_strokes):
            # Distance to start of the stroke
            dist_to_start = distance(current_point, stroke[0])
            if dist_to_start < min_dist:
                min_dist = dist_to_start
                best_stroke_index = i
                reverse_stroke = False
            
            # Distance to end of the stroke
            dist_to_end = distance(current_point, stroke[-1])
            if dist_to_end < min_dist:
                min_dist = dist_to_end
                best_stroke_index = i
                reverse_stroke = True

        # Get the best stroke and remove it from the remaining list
        best_stroke = remaining_strokes.pop(best_stroke_index)

        if reverse_stroke:
            best_stroke.reverse()
        
        optimized_path.append(best_stroke)
        current_point = best_stroke[-1]

    return optimized_path

def save_to_file(strokes, filename):
    """Saves the final toolpath to a text file."""
    with open(filename, 'w') as f:
        for stroke in strokes:
            if not stroke:
                continue
            
            # 1. Pen up, move to the start of the stroke
            start_point = stroke[0]
            f.write(f"MOVETO,{start_point[0]:.4f},{start_point[1]:.4f},{DOBOT_Z_MOVE:.4f}\n")
            
            # 2. Pen down
            f.write(f"LINETO,{start_point[0]:.4f},{start_point[1]:.4f},{DOBOT_Z_DRAW:.4f}\n")
            
            # 3. Draw the rest of the stroke
            for point in stroke[1:]:
                f.write(f"LINETO,{point[0]:.4f},{point[1]:.4f},{DOBOT_Z_DRAW:.4f}\n")
        
        # 4. Final pen up after the last stroke
        last_point = strokes[-1][-1]
        f.write(f"MOVETO,{last_point[0]:.4f},{last_point[1]:.4f},{DOBOT_Z_MOVE:.4f}\n")


def process_and_save(strokes, img_width, img_height, output_filename):
    """Main function to run the full optimization and saving process."""
    scaled_strokes = scale_strokes_to_dobot(strokes, img_width, img_height)
    optimized_strokes = optimize_path(scaled_strokes)
    save_to_file(optimized_strokes, output_filename)