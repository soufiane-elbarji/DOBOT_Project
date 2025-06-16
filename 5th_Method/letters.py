# letters.py
import numpy as np

def vertical_line(x, y, height, step):
    return [(x, y + i) for i in np.arange(0, height + step, step)]

def horizontal_line(x, y, width):
    return [(x + i, y) for i in np.arange(0, width + 1, 2)]

# Uppercase letters

def letter_A(x0, y0, h=40, w=20):
    return [[(x0, y0), (x0 + w/2, y0 + h), (x0 + w, y0)], [(x0 + w/4, y0 + h/2), (x0 + 3*w/4, y0 + h/2)]]

def letter_B(x0, y0, h=40, w=20):
    spine = vertical_line(x0, y0, h, 2)
    top = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + 3*h/4), (x0, y0 + h/2)]
    bottom = [(x0, y0 + h/2), (x0 + w, y0 + h/4), (x0 + w, y0), (x0, y0)]
    return [spine, top, bottom]

def letter_C(x0, y0, h=40, w=20):
    return [[(x0 + w, y0 + h), (x0, y0 + h), (x0, y0), (x0 + w, y0)]]

def letter_D(x0, y0, h=40, w=20):
    spine = vertical_line(x0, y0, h, 2)
    curve = [(x0, y0 + h), (x0 + w, y0 + 3*h/4), (x0 + w, y0 + h/4), (x0, y0)]
    return [spine, curve]

def letter_E(x0, y0, h=40, w=20):
    return [
        vertical_line(x0, y0, h, 2),
        horizontal_line(x0, y0 + h, w),
        horizontal_line(x0, y0 + h/2, w * 0.7),
        horizontal_line(x0, y0, w)
    ]

def letter_F(x0, y0, h=40, w=20):
    return [
        vertical_line(x0, y0, h, 2),
        horizontal_line(x0, y0 + h, w),
        horizontal_line(x0, y0 + h/2, w * 0.6)
    ]

def letter_G(x0, y0, h=40, w=20):
    return [[
        (x0 + w, y0 + h), (x0, y0 + h), (x0, y0), (x0 + w, y0),
        (x0 + w, y0 + h/2), (x0 + w/2, y0 + h/2)
    ]]

def letter_H(x0, y0, h=40, w=20):
    return [
        vertical_line(x0, y0, h, 2),
        vertical_line(x0 + w, y0, h, 2),
        horizontal_line(x0, y0 + h/2, w)
    ]

def letter_I(x0, y0, h=40):
    return [vertical_line(x0, y0, h, 2)]

def letter_J(x0, y0, h=40, w=20):
    return [[(x0 + w, y0 + h), (x0 + w, y0 + h/4), (x0, y0), (x0 - w/2, y0 + h/4)]]

def letter_K(x0, y0, h=40, w=20):
    return [
        vertical_line(x0, y0, h, 2),
        [(x0, y0 + h/2), (x0 + w, y0 + h)],
        [(x0, y0 + h/2), (x0 + w, y0)]
    ]

def letter_L(x0, y0, h=40, w=20):
    return [
        vertical_line(x0, y0, h, 2),
        horizontal_line(x0, y0, w)
    ]

def letter_M(x0, y0, h=40, w=20):
    return [[(x0, y0), (x0, y0 + h), (x0 + w/2, y0 + h/2), (x0 + w, y0 + h), (x0 + w, y0)]]

def letter_N(x0, y0, h=40, w=20):
    return [[(x0, y0), (x0, y0 + h), (x0 + w, y0), (x0 + w, y0 + h)]]

def letter_O(x0, y0, h=40, w=20, step_deg=10):
    cx = x0 + w/2
    cy = y0 + h/2
    r = min(w, h) / 2 * 0.9
    points = []
    for angle in np.arange(0, 360 + step_deg, step_deg):
        rad = np.radians(angle)
        x = cx + r * np.cos(rad)
        y = cy + r * np.sin(rad)
        points.append((x, y))
    return [points]

def letter_P(x0, y0, h=40, w=20):
    spine = vertical_line(x0, y0, h, 2)
    loop = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h/2), (x0, y0 + h/2)]
    return [spine, loop]

def letter_Q(x0, y0, h=40, w=20, step_deg=10):
    cx = x0 + w/2
    cy = y0 + h/2
    r = min(w, h) / 2 * 0.9
    points = []
    for angle in np.arange(0, 360 + step_deg, step_deg):
        rad = np.radians(angle)
        x = cx + r * np.cos(rad)
        y = cy + r * np.sin(rad)
        points.append((x, y))
    start_angle = 315
    start_x = cx + r * np.cos(np.radians(start_angle))
    start_y = cy + r * np.sin(np.radians(start_angle))
    end_x = cx + r * 1.5 * np.cos(np.radians(start_angle))
    end_y = cy + r * 1.5 * np.sin(np.radians(start_angle))
    tail = [(start_x, start_y), (end_x, end_y)]
    return [points, tail]

def letter_R(x0, y0, h=40, w=15, step=2):
    spine = vertical_line(x0, y0, h, step)
    loop = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h/2), (x0, y0 + h/2)]
    leg = [(x0, y0 + h/2), (x0 + w, y0)]
    return [spine, loop, leg]

def letter_S(x0, y0, h=40, w=20):
    top = [(x0 + w, y0 + h), (x0, y0 + h), (x0, y0 + h/2)]
    bottom = [(x0, y0 + h/2), (x0 + w, y0 + h/2), (x0 + w, y0), (x0, y0)]
    return [top, bottom]

def letter_T(x0, y0, h=40, w=20):
    top = horizontal_line(x0, y0 + h, w)
    spine = vertical_line(x0 + w / 2, y0, h, 2)
    return [top, spine]

def letter_U(x0, y0, h=40, w=20, step=2):
    left = vertical_line(x0, y0 + h/2, h/2, step)
    right = vertical_line(x0 + w, y0 + h/2, h/2, step)
    bottom = [(x0, y0), (x0 + w, y0)]
    return [left, bottom, right]

def letter_V(x0, y0, h=40, w=20):
    return [[(x0, y0 + h), (x0 + w / 2, y0), (x0 + w, y0 + h)]]

def letter_W(x0, y0, h=40, w=30):
    return [[(x0, y0 + h), (x0 + w/4, y0), (x0 + w/2, y0 + h/2), (x0 + 3*w/4, y0), (x0 + w, y0 + h)]]

def letter_X(x0, y0, h=40, w=20):
    diag1 = [(x0, y0), (x0 + w, y0 + h)]
    diag2 = [(x0, y0 + h), (x0 + w, y0)]
    return [diag1, diag2]

def letter_Y(x0, y0, h=40, w=20):
    arms = [(x0, y0 + h), (x0 + w/2, y0 + h/2), (x0 + w, y0 + h)]
    stem = [(x0 + w/2, y0 + h/2), (x0 + w/2, y0)]
    return [arms, stem]

def letter_Z(x0, y0, h=40, w=20):
    top = horizontal_line(x0, y0 + h, w)
    diag = [(x0 + w, y0 + h), (x0, y0)]
    bot = horizontal_line(x0, y0, w)
    return [top, diag, bot]

# Lowercase letters

def letter_a(x0, y0, h=30, w=15):
    circle = []
    for angle in np.arange(0, 360, 20):
        rad = np.radians(angle)
        circle.append((x0 + w/2 + (w/2)*np.cos(rad), y0 + h/2 + (h/2)*np.sin(rad)))
    stroke = [(x0 + w, y0), (x0 + w, y0 + h)]
    return [circle, stroke]

def letter_b(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    loop = [(x0, y0 + h/2), (x0 + w, y0 + h/2), (x0 + w, y0), (x0, y0)]
    return [spine, loop]

def letter_c(x0, y0, h=30, w=15):
    return [[(x0 + w, y0 + h), (x0, y0 + h), (x0, y0), (x0 + w, y0)]]

def letter_d(x0, y0, h=30, w=15):
    spine = vertical_line(x0 + w, y0, h, 2)
    loop = [(x0 + w, y0 + h), (x0, y0 + h), (x0, y0), (x0 + w, y0)]
    return [spine, loop]

def letter_e(x0, y0, h=30, w=15):
    top = horizontal_line(x0, y0 + h, w)
    middle = horizontal_line(x0, y0 + h/2, w*0.7)
    curve = [(x0 + w, y0 + h), (x0, y0 + h/2), (x0 + w, y0 + h/2), (x0, y0)]
    return [top, middle, curve]

def letter_f(x0, y0, h=30, w=15):
    spine = vertical_line(x0 + w/2, y0, h, 2)
    cross = horizontal_line(x0, y0 + 3*h/4, w)
    return [spine, cross]

def letter_g(x0, y0, h=30, w=15):
    loop = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0), (x0, y0)]
    tail = [(x0 + w, y0), (x0 + w*1.2, y0 - h/2), (x0, y0 - h/2)]
    return [loop, tail]

def letter_h(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    arch = [(x0, y0 + h/2), (x0 + w, y0 + h/2), (x0 + w, y0)]
    return [spine, arch]

def letter_i(x0, y0, h=30, w=15):
    stem = vertical_line(x0 + w/2, y0, h, 2)
    dot = [(x0 + w/2, y0 + h + 5), (x0 + w/2 + 2, y0 + h + 5)]
    return [stem, dot]

def letter_j(x0, y0, h=30, w=15):
    stem = [(x0 + w/2, y0 + h), (x0 + w/2, y0 - h/2)]
    curve = [(x0 + w/2, y0 - h/2), (x0, y0 - h/2)]
    return [stem, curve]

def letter_k(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    diag1 = [(x0, y0 + h/2), (x0 + w, y0 + h)]
    diag2 = [(x0, y0 + h/2), (x0 + w, y0)]
    return [spine, diag1, diag2]

def letter_l(x0, y0, h=30, w=15):
    return [vertical_line(x0 + w/2, y0, h, 2)]

def letter_m(x0, y0, h=30, w=15):
    return [[
        (x0, y0), (x0, y0 + h), (x0 + w/3, y0 + h/2),
        (x0 + 2*w/3, y0 + h), (x0 + 2*w/3, y0), (x0 + w, y0 + h)
    ]]

def letter_n(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    arch = [(x0, y0 + h), (x0 + w, y0), (x0 + w, y0 + h)]
    return [spine, arch]

def letter_o(x0, y0, h=30, w=15, step_deg=15):
    cx = x0 + w/2
    cy = y0 + h/2
    r = min(w, h) / 2 * 0.9
    points = []
    for angle in np.arange(0, 360 + step_deg, step_deg):
        rad = np.radians(angle)
        x = cx + r * np.cos(rad)
        y = cy + r * np.sin(rad)
        points.append((x, y))
    return [points]

def letter_p(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    loop = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h/2), (x0, y0 + h/2)]
    return [spine, loop]

def letter_q(x0, y0, h=30, w=15):
    loop = [(x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)]
    tail = [(x0 + w*0.7, y0), (x0 + w*1.3, y0 - h/2)]
    return [loop, tail]

def letter_r(x0, y0, h=30, w=15):
    spine = vertical_line(x0, y0, h, 2)
    loop = [(x0, y0 + h), (x0 + w, y0 + h), (x0 + w, y0 + h/2), (x0, y0 + h/2)]
    leg = [(x0, y0 + h/2), (x0 + w, y0)]
    return [spine, loop, leg]

def letter_s(x0, y0, h=30, w=15):
    top = [(x0 + w, y0 + h), (x0, y0 + h), (x0, y0 + h/2)]
    bottom = [(x0, y0 + h/2), (x0 + w, y0 + h/2), (x0 + w, y0), (x0, y0)]
    return [top, bottom]

def letter_t(x0, y0, h=30, w=15):
    spine = vertical_line(x0 + w/2, y0, h, 2)
    cross = horizontal_line(x0, y0 + 3*h/4, w)
    return [spine, cross]

def letter_u(x0, y0, h=30, w=15):
    left = vertical_line(x0, y0, h - 10, 2)
    right = vertical_line(x0 + w, y0, h - 10, 2)
    bottom = [(x0, y0), (x0 + w, y0)]
    return [left, bottom, right]

def letter_v(x0, y0, h=30, w=15):
    return [[(x0, y0 + h), (x0 + w/2, y0), (x0 + w, y0 + h)]]

def letter_w(x0, y0, h=30, w=20):
    return [[(x0, y0 + h), (x0 + w/4, y0), (x0 + w/2, y0 + h/2), (x0 + 3*w/4, y0), (x0 + w, y0 + h)]]

def letter_x(x0, y0, h=30, w=15):
    diag1 = [(x0, y0), (x0 + w, y0 + h)]
    diag2 = [(x0, y0 + h), (x0 + w, y0)]
    return [diag1, diag2]

def letter_y(x0, y0, h=30, w=15):
    arms = [(x0, y0 + h), (x0 + w/2, y0 + h/2), (x0 + w, y0 + h)]
    stem = [(x0 + w/2, y0 + h/2), (x0 + w/2, y0 - h/2)]
    return [arms, stem]

def letter_z(x0, y0, h=30, w=15):
    top = horizontal_line(x0, y0 + h, w)
    diag = [(x0 + w, y0 + h), (x0, y0)]
    bot = horizontal_line(x0, y0, w)
    return [top, diag, bot]

# Map characters to drawing functions
letter_funcs = {
    'A': letter_A, 'a': letter_a,
    'B': letter_B, 'b': letter_b,
    'C': letter_C, 'c': letter_c,
    'D': letter_D, 'd': letter_d,
    'E': letter_E, 'e': letter_e,
    'F': letter_F, 'f': letter_f,
    'G': letter_G, 'g': letter_g,
    'H': letter_H, 'h': letter_h,
    'I': letter_I, 'i': letter_i,
    'J': letter_J, 'j': letter_j,
    'K': letter_K, 'k': letter_k,
    'L': letter_L, 'l': letter_l,
    'M': letter_M, 'm': letter_m,
    'N': letter_N, 'n': letter_n,
    'O': letter_O, 'o': letter_o,
    'P': letter_P, 'p': letter_p,
    'Q': letter_Q, 'q': letter_q,
    'R': letter_R, 'r': letter_r,
    'S': letter_S, 's': letter_s,
    'T': letter_T, 't': letter_t,
    'U': letter_U, 'u': letter_u,
    'V': letter_V, 'v': letter_v,
    'W': letter_W, 'w': letter_w,
    'X': letter_X, 'x': letter_x,
    'Y': letter_Y, 'y': letter_y,
    'Z': letter_Z, 'z': letter_z
}

def text_to_strokes(text, x0=0, y0=0, h=30, w=15, letter_spacing=20, line_spacing=40):
    strokes = []
    cursor_x = x0
    cursor_y = y0

    for ch in text:
        if ch == '\n':
            cursor_x = x0
            cursor_y -= line_spacing
            continue

        f = letter_funcs.get(ch)  # Case-sensitive lookup
        if f:
            letter_strokes = f(cursor_x, cursor_y, h, w)
            strokes.extend(letter_strokes)
            cursor_x += letter_spacing
        else:
            # Unknown char, just move cursor (space etc.)
            cursor_x += letter_spacing

    return strokes