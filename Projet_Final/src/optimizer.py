import numpy as np
import math

OUTPUT_TOOLPATH_FILE = "temp/toolpath.txt"  # Output file for the toolpath

def scale_strokes_to_dobot(strokes, img_width, img_height, DOBOT_X_MIN, DOBOT_X_MAX, DOBOT_Y_MIN, DOBOT_Y_MAX):
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

# def distance(p1, p2):
#     return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

# def optimize_path(paths):
#     if not paths:
#         return []

#     remaining = paths.copy()
#     ordered = [remaining.pop(0)]

#     while remaining:
#         last_point = ordered[-1][-1]

#         for i, path in enumerate(remaining):
#             d = distance(last_point, path[0])
#             # print(f"Path {i} starts at {path[0]} — distance = {d:.2f}")

#         next_index = min(
#             range(len(remaining)),
#             key=lambda i: distance(last_point, remaining[i][0])
#         )
#         chosen_path = remaining.pop(next_index)
#         # print(f"Chose path starting at {chosen_path[0]}")
#         ordered.append(chosen_path)

#     return ordered

def save_to_file(strokes, DOBOT_Z_MOVE, DOBOT_Z_DRAW):
    """Saves the final toolpath to a text file."""
    with open(OUTPUT_TOOLPATH_FILE, 'w') as f:
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