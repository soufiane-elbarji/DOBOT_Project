import math

def bezier_curve(start, control1, control2, end, num_points=10):
    """Generate points along a cubic Bézier curve"""
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        t2 = t * t
        t3 = t2 * t
        mt = 1 - t
        mt2 = mt * mt
        mt3 = mt2 * mt
        
        x = mt3 * start[0] + 3 * mt2 * t * control1[0] + 3 * mt * t2 * control2[0] + t3 * end[0]
        y = mt3 * start[1] + 3 * mt2 * t * control1[1] + 3 * mt * t2 * control2[1] + t3 * end[1]
        points.append((x, y))
    
    return points

def quadratic_curve(start, control, end, num_points=8):
    """Generate points along a quadratic Bézier curve"""
    points = []
    for i in range(num_points + 1):
        t = i / num_points
        t2 = t * t
        mt = 1 - t
        mt2 = mt * mt
        
        x = mt2 * start[0] + 2 * mt * t * control[0] + t2 * end[0]
        y = mt2 * start[1] + 2 * mt * t * control[1] + t2 * end[1]
        points.append((x, y))
    
    return points

def arc_to_points(center, radius, start_angle, end_angle, num_points=8):
    """Generate points along an arc"""
    points = []
    angle_range = end_angle - start_angle
    for i in range(num_points + 1):
        angle = start_angle + (i / num_points) * angle_range
        x = center[0] + radius * math.cos(math.radians(angle))
        y = center[1] + radius * math.sin(math.radians(angle))
        points.append((x, y))
    return points

# Complete alphabet with both uppercase and lowercase letters
# Lowercase letters are designed to fit in a 5x7 grid (7 units tall, 5 wide)
# with baseline at y=0 and ascenders going to y=10, descenders to y=-3
alphabet = {
    # UPPERCASE LETTERS
    'A': [
        [(0, 0), (2.5, 10)],
        [(2.5, 10), (5, 0)],
        [(1, 3.5), (4, 3.5)]
    ],
    
    'B': [
        [(0, 0), (0, 10)],
        bezier_curve((0, 10), (2, 10), (4, 9), (4, 7.5), 8),
        bezier_curve((4, 7.5), (4, 6), (2, 5), (0, 5), 6),
        bezier_curve((0, 5), (2.5, 5), (4.5, 4), (4.5, 2.5), 6),
        bezier_curve((4.5, 2.5), (4.5, 1), (2.5, 0), (0, 0), 8)
    ],
    
    'C': [
        bezier_curve((5, 2), (3, 0), (2, 0), (0, 2), 6) +
        [(0, 2), (0, 8)] +
        bezier_curve((0, 8), (2, 10), (3, 10), (5, 8), 6)
    ],
    
    'D': [
        [(0, 0), (0, 10)],
        bezier_curve((0, 10), (2, 10), (4, 8), (4, 5), 8) +
        bezier_curve((4, 5), (4, 2), (2, 0), (0, 0), 8)
    ],
    
    'E': [
        [(5, 0), (0, 0)],
        [(0, 0), (0, 10)],
        [(0, 10), (4.5, 10)],
        [(0, 5), (3.5, 5)]
    ],
    
    'F': [
        [(0, 0), (0, 10)],
        [(0, 10), (4.5, 10)],
        [(0, 5.5), (3.5, 5.5)]
    ],
    
    'G': [
        bezier_curve((5, 2), (3, 0), (2, 0), (0, 2), 6) +
        [(0, 2), (0, 8)] +
        bezier_curve((0, 8), (2, 10), (3, 10), (5, 8), 6),
        [(5, 8), (5, 5)],
        [(5, 5), (3, 5)]
    ],
    
    'H': [
        [(0, 0), (0, 10)],
        [(5, 0), (5, 10)],
        [(0, 5), (5, 5)]
    ],
    
    'I': [
        [(1, 0), (4, 0)],
        [(2.5, 0), (2.5, 10)],
        [(1, 10), (4, 10)]
    ],
    
    'J': [
        [(4, 10), (4, 3)] +
        bezier_curve((4, 3), (4, 1), (3, 0), (1.5, 0), 6) +
        bezier_curve((1.5, 0), (0.5, 0), (0, 1), (0, 2), 4)
    ],
    
    'K': [
        [(0, 0), (0, 10)],
        [(0, 4), (3, 10)],
        [(0, 4), (4, 0)]
    ],
    
    'L': [
        [(0, 10), (0, 0)],
        [(0, 0), (4.5, 0)]
    ],
    
    'M': [
        [(0, 0), (0, 10)],
        [(0, 10), (2.5, 6)],
        [(2.5, 6), (5, 10)],
        [(5, 10), (5, 0)]
    ],
    
    'N': [
        [(0, 0), (0, 10)],
        [(0, 10), (5, 0)],
        [(5, 0), (5, 10)]
    ],
    
    'O': [
        bezier_curve((0, 5), (0, 8), (2, 10), (2.5, 10), 6) +
        bezier_curve((2.5, 10), (3, 10), (5, 8), (5, 5), 6) +
        bezier_curve((5, 5), (5, 2), (3, 0), (2.5, 0), 6) +
        bezier_curve((2.5, 0), (2, 0), (0, 2), (0, 5), 6)
    ],
    
    'P': [
        [(0, 0), (0, 10)],
        bezier_curve((0, 10), (2, 10), (4, 9), (4, 7.5), 8) +
        bezier_curve((4, 7.5), (4, 6), (2, 5), (0, 5), 6)
    ],
    
    'Q': [
        bezier_curve((0, 5), (0, 8), (2, 10), (2.5, 10), 6) +
        bezier_curve((2.5, 10), (3, 10), (5, 8), (5, 5), 6) +
        bezier_curve((5, 5), (5, 2), (3, 0), (2.5, 0), 6) +
        bezier_curve((2.5, 0), (2, 0), (0, 2), (0, 5), 6),
        [(3.5, 2.5), (5.5, 0)]
    ],
    
    'R': [
        [(0, 0), (0, 10)],
        bezier_curve((0, 10), (2, 10), (4, 9), (4, 7.5), 8) +
        bezier_curve((4, 7.5), (4, 6), (2, 5), (0, 5), 6),
        [(2, 5), (4.5, 0)]
    ],
    
    'S': [
        bezier_curve((4.5, 1.5), (3, 0), (2, 0), (0.5, 1.5), 6) +
        bezier_curve((0.5, 1.5), (0.5, 3), (1.5, 4), (2.5, 5), 6) +
        bezier_curve((2.5, 5), (3.5, 6), (4.5, 7), (4.5, 8.5), 6) +
        bezier_curve((4.5, 8.5), (3, 10), (2, 10), (0.5, 8.5), 6)
    ],
    
    'T': [
        [(0.5, 10), (4.5, 10)],
        [(2.5, 10), (2.5, 0)]
    ],
    
    'U': [
        [(0, 10), (0, 3)] +
        bezier_curve((0, 3), (0, 1), (1.5, 0), (2.5, 0), 8) +
        bezier_curve((2.5, 0), (3.5, 0), (5, 1), (5, 3), 8),
        [(5, 3), (5, 10)]
    ],
    
    'V': [
        [(0, 10), (2.5, 0)],
        [(2.5, 0), (5, 10)]
    ],
    
    'W': [
        [(0, 10), (1, 0)],
        [(1, 0), (2.5, 6)],
        [(2.5, 6), (4, 0)],
        [(4, 0), (5, 10)]
    ],
    
    'X': [
        [(0, 0), (5, 10)],
        [(0, 10), (5, 0)]
    ],
    
    'Y': [
        [(0, 10), (2.5, 5)],
        [(5, 10), (2.5, 5)],
        [(2.5, 5), (2.5, 0)]
    ],
    
    'Z': [
        [(0, 10), (5, 10)],
        [(5, 10), (0, 0)],
        [(0, 0), (5, 0)]
    ],

    # LOWERCASE LETTERS
    'a': [
        # Circular part
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (2.5, 7), 6) +
        bezier_curve((2.5, 7), (3.5, 7), (4.5, 6.5), (4.5, 5.5), 6) +
        bezier_curve((4.5, 5.5), (4.5, 4.5), (3.5, 4), (2.5, 4), 6) +
        bezier_curve((2.5, 4), (1.5, 4), (0.5, 4.5), (0.5, 5.5), 6),
        # Vertical line
        [(4.5, 7), (4.5, 0)]
    ],
    
    'b': [
        # Vertical line
        [(0.5, 0), (0.5, 10)],
        # Curved part
        bezier_curve((0.5, 7), (1.5, 7), (3.5, 6.5), (3.5, 5.5), 6) +
        bezier_curve((3.5, 5.5), (3.5, 4.5), (1.5, 4), (0.5, 4), 6)
    ],
    
    'c': [
        bezier_curve((3.5, 4.5), (2.5, 4), (1.5, 4), (0.5, 4.5), 6) +
        bezier_curve((0.5, 4.5), (0.5, 6.5), (1.5, 7), (2.5, 7), 6) +
        bezier_curve((2.5, 7), (3, 7), (3.5, 6.5), (3.5, 6), 4)
    ],
    
    'd': [
        # Curved part
        bezier_curve((3.5, 4), (1.5, 4), (0.5, 4.5), (0.5, 5.5), 6) +
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (3.5, 7), 6),
        # Vertical line
        [(3.5, 0), (3.5, 10)]
    ],
    
    'e': [
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (2.5, 7), 6) +
        bezier_curve((2.5, 7), (3.5, 7), (4, 6), (4, 5.5), 6),
        [(0.5, 5.5), (4, 5.5)],
        bezier_curve((4, 5.5), (3.5, 4), (2.5, 4), (1.5, 4), 4)
    ],
    
    'f': [
        # Curved top
        bezier_curve((3, 10), (2, 10), (1, 9), (1, 8), 6),
        [(1, 8), (1, 0)],
        [(0, 6), (2.5, 6)]
    ],
    
    'g': [
        # Circular part
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (2.5, 7), 6) +
        bezier_curve((2.5, 7), (3.5, 7), (4, 6.5), (4, 5.5), 6) +
        bezier_curve((4, 5.5), (4, 4.5), (3.5, 4), (2.5, 4), 6) +
        bezier_curve((2.5, 4), (1.5, 4), (0.5, 4.5), (0.5, 5.5), 6),
        # Descender
        [(4, 4), (4, -1)] +
        bezier_curve((4, -1), (3, -2), (2, -2), (1, -1), 4)
    ],
    
    'h': [
        [(0.5, 0), (0.5, 10)],
        bezier_curve((0.5, 7), (1.5, 7), (3, 6.5), (3.5, 5.5), 6),
        [(3.5, 5.5), (3.5, 0)]
    ],
    
    'i': [
        [(1.5, 0), (1.5, 7)],
        [(1.5, 8.5), (1.5, 9)]  # dot
    ],
    
    'j': [
        [(2, 7), (2, -1)] +
        bezier_curve((2, -1), (1.5, -2), (1, -2), (0.5, -1.5), 4),
        [(2, 8.5), (2, 9)]  # dot
    ],
    
    'k': [
        [(0.5, 0), (0.5, 10)],
        [(0.5, 4.5), (2.5, 7)],
        [(1.5, 5.5), (3, 4)]
    ],
    
    'l': [
        [(1.5, 0), (1.5, 10)]
    ],
    
    'm': [
        [(0.5, 0), (0.5, 7)],
        bezier_curve((0.5, 7), (1, 7), (1.5, 6.5), (2, 6), 4),
        [(2, 6), (2, 0)],
        bezier_curve((2, 7), (2.5, 7), (3, 6.5), (3.5, 6), 4),
        [(3.5, 6), (3.5, 0)]
    ],
    
    'n': [
        [(0.5, 0), (0.5, 7)],
        bezier_curve((0.5, 7), (1.5, 7), (3, 6.5), (3.5, 5.5), 6),
        [(3.5, 5.5), (3.5, 0)]
    ],
    
    'o': [
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (2.5, 7), 6) +
        bezier_curve((2.5, 7), (3.5, 7), (4.5, 6.5), (4.5, 5.5), 6) +
        bezier_curve((4.5, 5.5), (4.5, 4.5), (3.5, 4), (2.5, 4), 6) +
        bezier_curve((2.5, 4), (1.5, 4), (0.5, 4.5), (0.5, 5.5), 6)
    ],
    
    'p': [
        [(0.5, -3), (0.5, 7)],
        bezier_curve((0.5, 7), (1.5, 7), (3.5, 6.5), (3.5, 5.5), 6) +
        bezier_curve((3.5, 5.5), (3.5, 4.5), (1.5, 4), (0.5, 4), 6)
    ],
    
    'q': [
        bezier_curve((0.5, 5.5), (0.5, 6.5), (1.5, 7), (3.5, 7), 6) +
        bezier_curve((3.5, 7), (3.5, 4.5), (1.5, 4), (0.5, 4.5), 4),
        [(3.5, 7), (3.5, -3)]
    ],
    
    'r': [
        [(0.5, 0), (0.5, 7)],
        bezier_curve((0.5, 7), (1.5, 7), (2.5, 6.5), (3, 6), 4)
    ],
    
    's': [
        bezier_curve((3.5, 4.5), (2.5, 4), (1.5, 4), (0.5, 4.5), 4) +
        bezier_curve((0.5, 4.5), (1, 5.5), (2, 5.5), (2.5, 5.5), 4) +
        bezier_curve((2.5, 5.5), (3.5, 6), (3.5, 6.5), (2.5, 7), 4) +
        bezier_curve((2.5, 7), (1.5, 7), (0.5, 6.5), (0.5, 6), 4)
    ],
    
    't': [
        [(1.5, 9), (1.5, 2)] +
        bezier_curve((1.5, 2), (1.5, 1), (2, 0.5), (2.5, 0.5), 4),
        [(0.5, 6.5), (3, 6.5)]
    ],
    
    'u': [
        [(0.5, 7), (0.5, 2)] +
        bezier_curve((0.5, 2), (0.5, 1), (1.5, 0.5), (2.5, 0.5), 6) +
        bezier_curve((2.5, 0.5), (3.5, 0.5), (4, 1), (4, 2), 6),
        [(4, 2), (4, 7)]
    ],
    
    'v': [
        [(0.5, 7), (2, 0)],
        [(2, 0), (3.5, 7)]
    ],
    
    'w': [
        [(0.5, 7), (1, 0)],
        [(1, 0), (2, 4)],
        [(2, 4), (3, 0)],
        [(3, 0), (3.5, 7)]
    ],
    
    'x': [
        [(0.5, 7), (3.5, 0)],
        [(0.5, 0), (3.5, 7)]
    ],
    
    'y': [
        [(0.5, 7), (2, 2)],
        [(3.5, 7), (2, 2), (1.5, -1)] +
        bezier_curve((1.5, -1), (1, -2), (0.5, -2), (0, -1.5), 4)
    ],
    
    'z': [
        [(0.5, 7), (3.5, 7)],
        [(3.5, 7), (0.5, 0)],
        [(0.5, 0), (3.5, 0)]
    ],
    
    # PUNCTUATION
    '.': [
        [(1.5, 0), (1.5, 0.5)]
    ],
    
    ',': [
        [(1.5, 0), (1.5, 0.5)],
        [(1.5, 0.5), (1, -1)]
    ],
    
    '!': [
        [(1.5, 2), (1.5, 10)],
        [(1.5, 0), (1.5, 0.5)]
    ],
    
    '?': [
        bezier_curve((0.5, 8), (0.5, 10), (2.5, 10), (3.5, 8), 6) +
        bezier_curve((3.5, 8), (3.5, 6), (1.5, 5), (1.5, 3), 6),
        [(1.5, 0), (1.5, 0.5)]
    ],
    
    "'": [
        [(1.5, 8), (1, 10)]
    ],
    
    '-': [
        [(0.5, 5), (3.5, 5)]
    ],
    
    # Space character
    ' ': []
}

def convert_to_dobot_format():
    """Convert the curved alphabet to the format expected by your Dobot code"""
    dobot_alphabet = {}
    
    for letter, strokes in alphabet.items():
        dobot_strokes = []
        
        for stroke in strokes:
            if len(stroke) >= 2:  # Valid stroke with at least 2 points
                dobot_strokes.append(stroke)
        
        dobot_alphabet[letter] = dobot_strokes
    
    return dobot_alphabet

# Generate the final alphabet for the Dobot
dobot_alphabet = convert_to_dobot_format()