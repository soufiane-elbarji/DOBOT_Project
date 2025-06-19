import json, time, re, sys, string
import speech_recognition as sr
from openai import OpenAI
import numpy as np
from serial.tools import list_ports
import pydobot
from Alphabet import alphabet  # <- import the dictionary

# ── CONFIG ─────────────────────────────────────
DEEPSEEK_API_KEY = "API_KEY"
FONT_HEIGHT_MM  = 6.0
PEN_UP_Z        = -40
PEN_DOWN_Z      = -64
START_X         = 240 
START_Y         = 135
SPEED_MM_S      = 50
CHAR_SPACING    = 6
line_spacing    = FONT_HEIGHT_MM * 2
ALLOWED_CHARS   = string.ascii_uppercase + " "

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=DEEPSEEK_API_KEY)

# ── STROKE FUNCTIONS ───────────────────────────
def sanitize(text):
    return ''.join(ch if ch.upper() in ALLOWED_CHARS else ' ' for ch in text)

def text_to_custom_strokes(text, height_mm):
    scale = height_mm / 10.0  # original letters are designed in 10x10
    strokes = []
    cursor_x = 0.0

    for char in text.upper():
        if char == " ":
            cursor_x += CHAR_SPACING  # espace vide
            continue
        if char not in alphabet:
            cursor_x += CHAR_SPACING
            continue
        letter_strokes = []
        for segment in alphabet[char]:
            segment_scaled = [((x1 * scale) + cursor_x, y1 * scale) for (x1, y1) in segment]
            letter_strokes.append(segment_scaled)
        strokes.extend(letter_strokes)
        cursor_x += CHAR_SPACING  # move to next char
    return strokes

# ── VOICE AND AI FUNCTIONS ─────────────────────
def listen():
    r, mic = sr.Recognizer(), sr.Microphone()
    print("Speak your request…")
    with mic as src:
        r.adjust_for_ambient_noise(src)
        audio = r.listen(src)
    try:
        return r.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        print("Could not understand.")
        return None
    except sr.RequestError:
        print("Google API error.")
        return None

def extract_keyword(cmd):
    cmd = cmd.lower()
    m = re.search(r"about\s+(.+)$", cmd)
    return (m.group(1) if m else cmd).strip()

def generate_poem(keyword):
    prompt = (
        "You are an English poet. Write a short rhymed couplet of exactly two lines, "
        "no title, no extra text, max 16 words total. Topic: {}".format(keyword)
    )
    rsp = client.chat.completions.create(
        model="deepseek/deepseek-r1-0528:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return rsp.choices[0].message.content.strip()

# ── DOBOT CONTROL ───────────────────────────────
def write_strokes_with_dobot(strokes):
    
    port = "COM5"
    print("Connecting to Dobot on", port)

    device = pydobot.Dobot(port=port, verbose=False)
    device.speed = SPEED_MM_S
    device.move_to(START_X, START_Y, PEN_UP_Z, 0, wait=True)

    for stroke in strokes:
        if not stroke:
            continue
        x0, y0 = stroke[0]
        device.move_to(START_X + x0, START_Y + y0, PEN_UP_Z, 0, wait=True)
        device.move_to(START_X + x0, START_Y + y0, PEN_DOWN_Z, 0, wait=True)
        for x, y in stroke[1:]:
            device.move_to(START_X + x, START_Y + y, PEN_DOWN_Z, 0, wait=True)
        device.move_to(START_X + x, START_Y + y, PEN_UP_Z, 0, wait=True)

    device.move_to(START_X, START_Y, PEN_UP_Z, 0, wait=True)
    device.close()
    print("Poem written.")

def rotate_strokes_90_right(strokes):
    return [[(y, -x) for (x, y) in stroke] for stroke in strokes]

# ── MAIN PROGRAM ────────────────────────────────
def main():
    cmd = listen()
    if not cmd:
        return

    keyword = extract_keyword(cmd)
    print("Keyword:", keyword)

    poem = generate_poem(keyword)
    print("Poem:\n" + poem)

    poem_clean = sanitize(poem.strip().upper())
    strokes = []
    line_index = 0

    for line in poem_clean.splitlines():
        line_strokes = text_to_custom_strokes(line, FONT_HEIGHT_MM)

        rotated_strokes = rotate_strokes_90_right(line_strokes)

        offset_line = [[(x + line_index * line_spacing, y) for (x, y) in segment] for segment in rotated_strokes]

        strokes.extend(offset_line)
        line_index -= 1

    write_strokes_with_dobot(strokes)


if __name__ == "_main_":
    main()