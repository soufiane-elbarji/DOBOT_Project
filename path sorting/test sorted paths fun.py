import math


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def sort_paths_proximity(paths):
    if not paths:
        return []

    remaining = paths.copy()
    ordered = [remaining.pop(0)]

    while remaining:
        last_point = ordered[-1][-1]

        for i, path in enumerate(remaining):
            d = distance(last_point, path[0])
            print(f"Path {i} starts at {path[0]} — distance = {d:.2f}")

        next_index = min(
            range(len(remaining)),
            key=lambda i: distance(last_point, remaining[i][0])
        )
        chosen_path = remaining.pop(next_index)
        print(f"Chose path starting at {chosen_path[0]}")
        ordered.append(chosen_path)

    return ordered


paths = [
    [(0, 0), (1, 1)],
    [(5, 5), (6, 6)],
    [(2, 2), (3, 3)],
    [(10, 10), (11, 11)]
]


ordered_paths = sort_paths_proximity(paths)


print("\nOrdered Paths:")
for i, path in enumerate(ordered_paths):
    print(f"Path {i}: {path}")
