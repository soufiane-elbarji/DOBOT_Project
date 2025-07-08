import re
import string
import speech_recognition as sr
from openai import OpenAI
import numpy as np
from serial.tools import list_ports
import pydobot
from alphabet import dobot_alphabet  # Import the alphabet from our separate file

# ── CONFIG ─────────────────────────────────────
port = "COM5"  # Update this to match your Dobot's port
print("Connecting to Dobot on", port)

device = pydobot.Dobot(port=port, verbose=False)

(x, y, z, r, j1, j2, j3, j4) = device.pose()

SPEED_MM_S = 50
device.speed = SPEED_MM_S

DEEPSEEK_API_KEY = "API_KEY"
FONT_HEIGHT_MM  = 6.0
PEN_UP_Z        = z+20
PEN_DOWN_Z      = z
START_X         = x
START_Y         = y
CHAR_SPACING    = 6
line_spacing    = FONT_HEIGHT_MM * 2

# Updated to include lowercase letters and punctuation
ALLOWED_CHARS   = string.ascii_uppercase + string.ascii_lowercase + " .,!?'-"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=DEEPSEEK_API_KEY)

# ── STROKE FUNCTIONS ───────────────────────────
def sanitize(text):
    """Clean text to only include supported characters"""
    return ''.join(ch if ch in ALLOWED_CHARS else ' ' for ch in text)

def text_to_custom_strokes(text, height_mm):
    """Convert text to stroke paths using the curved alphabet"""
    scale = height_mm / 10.0  # original letters are designed in 10x10
    strokes = []
    cursor_x = 0.0

    for char in text:  # Keep original case
        if char == " ":
            cursor_x += CHAR_SPACING  # space
            continue
        if char not in dobot_alphabet:
            cursor_x += CHAR_SPACING
            continue
            
        # Get the stroke data for this character
        for stroke_points in dobot_alphabet[char]:
            if not stroke_points:  # Skip empty strokes
                continue
                
            # Scale and translate the stroke points
            scaled_stroke = []
            for point in stroke_points:
                scaled_point = (point[0] * scale + cursor_x, point[1] * scale)
                scaled_stroke.append(scaled_point)
            
            if scaled_stroke:
                strokes.append(scaled_stroke)
                
        cursor_x += CHAR_SPACING  # move to next char
    return strokes

def rotate_strokes_90_right(strokes):
    """Rotate all strokes 90 degrees clockwise (right)"""
    rotated_strokes = []
    for stroke in strokes:
        rotated_stroke = []
        for x, y in stroke:
            # Rotate 90 degrees right: (x, y) -> (y, -x)
            rotated_stroke.append((y, -x))
        rotated_strokes.append(rotated_stroke)
    return rotated_strokes

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
    
    device.move_to(START_X, START_Y, PEN_UP_Z, 0, wait=True)

    for stroke in strokes:
        if not stroke:
            continue
            
        # Move to start of stroke with pen up
        x0, y0 = stroke[0]
        device.move_to(START_X + x0, START_Y + y0, PEN_UP_Z, 0, wait=True)
        
        # Put pen down
        device.move_to(START_X + x0, START_Y + y0, PEN_DOWN_Z, 0, wait=True)
        
        # Draw the rest of the stroke
        for x, y in stroke[1:]:
            device.move_to(START_X + x, START_Y + y, PEN_DOWN_Z, 0, wait=True)
        
        # Lift pen up
        device.move_to(START_X + x, START_Y + y, PEN_UP_Z, 0, wait=True)

    device.close()
    print("Writing completed!")

# ── MAIN FUNCTION ──────────────────────────────
def main():
    print("Dobot Poetry Writer - Voice-Activated")
    print("Say: 'Write a poem about [topic]'")
    
    cmd = listen()
    if not cmd:
        print("No command received.")
        return
    
    keyword = extract_keyword(cmd)
    print("Keyword:", keyword)
    
    poem = generate_poem(keyword)
    print("Poem:\n" + poem)
    
    # Keep original case for better readability
    poem_clean = sanitize(poem.strip())
    strokes = []
    line_index = 0
    
    for line in poem_clean.splitlines():
        if not line.strip():  # Skip empty lines
            continue
            
        line_strokes = text_to_custom_strokes(line, FONT_HEIGHT_MM)
        
        rotated_strokes = rotate_strokes_90_right(line_strokes)
        
        # Offset each line by line_spacing
        offset_line = [[(x + line_index * line_spacing, y) for (x, y) in segment] for segment in rotated_strokes]
        
        strokes.extend(offset_line)
        line_index -= 1  # Move to next line position
    
    print(f"Generated {len(strokes)} strokes for writing")
    write_strokes_with_dobot(strokes)

if __name__ == "__main__":
    main()