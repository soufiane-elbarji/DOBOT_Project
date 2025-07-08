import json, time, subprocess, re, sys, string
import speech_recognition as sr
from openai import OpenAI
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
import numpy as np

# ── CONFIG ─────────────────────────────────────
DEEPSEEK_API_KEY = ""
JSON_PATH       = "text_to_write.json"
FONT_HEIGHT_MM  = 5.0
PEN_UP_Z        = -40
PEN_DOWN_Z      = -59
FONT            = FontProperties(family='HersheySimplex')
# ───────────────────────────────────────────────

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=DEEPSEEK_API_KEY)

ALLOWED_CHARS = string.ascii_letters + string.digits + " .,:;!?'-"

def listen():
    r, mic = sr.Recognizer(), sr.Microphone()
    print("Speak your request …")
    with mic as src:
        r.adjust_for_ambient_noise(src)
        audio = r.listen(src)
    try:
        return r.recognize_google(audio, language="en-US")
    except sr.UnknownValueError:
        print("Speech not understood.")
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

def sanitize(text):
    return ''.join(ch if ch in ALLOWED_CHARS or ch == '\n' else ' ' for ch in text)

def path_to_strokes(text, height_mm):
    text_path = TextPath((0, 0), text, prop=FONT, size=1)
    verts = text_path.vertices
    codes = text_path.codes

    # Scale path to desired height
    bbox = text_path.get_extents()
    scale = height_mm / bbox.height
    verts = verts * scale

    # Extract strokes
    strokes = []
    current_stroke = []
    for v, c in zip(verts, codes):
        if c == 1:  # MOVETO
            if current_stroke:
                strokes.append(current_stroke)
                current_stroke = []
            current_stroke.append(v.tolist())
        elif c == 2:  # LINETO
            current_stroke.append(v.tolist())
        elif c == 79:  # CLOSEPOLY
            pass
    if current_stroke:
        strokes.append(current_stroke)

    return strokes

# ── MAIN FLOW ────────────────────────────────────
cmd = listen()
if not cmd:
    sys.exit()

keyword = extract_keyword(cmd)
print("Keyword:", keyword)

poem = generate_poem(keyword)
print("Poem:\n" + poem)

poem_clean = sanitize(poem.strip())
stroke_paths = []
cursor_y = 0.0
line_spacing = FONT_HEIGHT_MM * 1.6

for line in poem_clean.splitlines():
    line_strokes = path_to_strokes(line, FONT_HEIGHT_MM)
    # Offset each line vertically
    offset_strokes = []
    for stroke in line_strokes:
        offset_strokes.append([[pt[0], pt[1] + cursor_y] for pt in stroke])
    stroke_paths.extend(offset_strokes)
    cursor_y -= line_spacing

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(stroke_paths, f)

print("Stroke paths saved to", JSON_PATH)
time.sleep(1)

subprocess.run(["py", "-3.5", "C:\\Users\\pc\\Documents\\GitHub\\DOBOT_Project\\3rd_Method\\write_with_dobot.py",    # change this to your local path
                "--json", JSON_PATH,
                "--upZ", str(PEN_UP_Z),
                "--downZ", str(PEN_DOWN_Z)])
