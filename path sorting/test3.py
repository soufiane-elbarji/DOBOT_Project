import math
from svgpathtools import svg2paths
import matplotlib.pyplot as plt

# -------------- Load and Convert Paths ----------------

def path_to_points(path, num_points=10):
    return [(seg.point(i / num_points).real, seg.point(i / num_points).imag)
            for seg in path for i in range(num_points + 1)]

def load_svg_paths(file_path):
    paths, _ = svg2paths(file_path)
    return [path_to_points(p) for p in paths if len(p) > 0]

def load_paths_from_txt(filename):
    paths = []
    current_path = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                if current_path:
                    paths.append(current_path)
                    current_path = []
            elif line:
                x, y = map(float, line.split(','))
                current_path.append((x, y))
    if current_path:
        paths.append(current_path)

    return paths

# -------------- Utility Functions ----------------

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def sort_paths_proximity(paths):
    if not paths:
        return []

    remaining = paths.copy()
    ordered = [remaining.pop(0)]

    while remaining:
        last_point = ordered[-1][-1]
        next_index = min(range(len(remaining)), key=lambda i: distance(last_point, remaining[i][0]))
        ordered.append(remaining.pop(next_index))

    return ordered

def draw_paths(paths, color='blue', label=''):
    for path in paths:
        x, y = zip(*path)
        plt.plot(x, y, color=color)
    if label:
        plt.title(label)

def save_paths_to_txt(paths, filename):
    with open(filename, 'w') as f:
        for i, path in enumerate(paths):
            f.write(f"# Path {i}\n")
            for x, y in path:
                f.write(f"{x:.3f}, {y:.3f}\n")
            f.write("\n")  

def normalize_paths(paths, target_width=200, target_height=200, margin=10):
    all_x = [x for path in paths for (x, _) in path]
    all_y = [y for path in paths for (_, y) in path]

    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    scale_x = (target_width - 2 * margin) / (max_x - min_x)
    scale_y = (target_height - 2 * margin) / (max_y - min_y)
    scale = min(scale_x, scale_y)

    normalized = []
    for path in paths:
        new_path = []
        for x, y in path:
            new_x = (x - min_x) * scale + margin
            new_y = (y - min_y) * scale + margin
            new_path.append((new_x, new_y))
        normalized.append(new_path)

    return normalized


raw_paths = load_svg_paths(svg_file)
ordered_paths = sort_paths_proximity(raw_paths)

# 2. Save sorted paths (unsclaed) for reference
save_paths_to_txt(ordered_paths, "sorted_paths.txt")
print("✅ Sorted SVG paths saved to sorted_paths.txt")

# 3. Scale the sorted paths for Dobot use
scaled_paths = normalize_paths(ordered_paths, target_width=250, target_height=250)
save_paths_to_txt(scaled_paths, "scaled_paths_for_dobot.txt")
print("✅ Scaled and Dobot-ready paths saved to scaled_paths_for_dobot.txt")

# 4. Plot (optional)
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
draw_paths(raw_paths, color='gray', label='Original Order')
plt.subplot(1, 2, 2)
draw_paths(ordered_paths, color='red', label='Sorted by Proximity')
plt.axis('equal')
plt.show()
