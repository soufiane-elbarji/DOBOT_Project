import speech_recognition as sr
from openai import OpenAI
from serial.tools import list_ports
import pydobot
import re
import string

from letters import text_to_strokes

# ── CONFIG ─────────────────────────────────────
DEEPSEEK_API_KEY = ""
FONT_HEIGHT = 30
FONT_WIDTH = 15
PEN_UP_Z = -40
PEN_DOWN_Z = -59
START_X = 200
START_Y = 0
SPEED_MM_S = 50
LETTER_SPACING = 20
LINE_SPACING = 40
ALLOWED_CHARS = string.ascii_letters + string.digits + " .,:;!?'-\n"

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=DEEPSEEK_API_KEY)

def sanitize(text):
    return ''.join(ch if ch in ALLOWED_CHARS else ' ' for ch in text.lower())

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

def write_strokes_with_dobot(strokes):
    ports = list_ports.comports()
    if not ports:
        print("No Dobot found.")
        return
    port = ports[0].device
    print("Connecting to Dobot on", port)

    device = pydobot.Dobot(port=port, verbose=True)
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

def main():
    cmd = listen()
    if not cmd:
        return

    keyword = extract_keyword(cmd)
    print("Keyword:", keyword)

    poem = generate_poem(keyword)
    print("Poem:\n" + poem)

    poem_clean = sanitize(poem.strip())

    strokes = text_to_strokes(poem_clean, x0=0, y0=0, h=FONT_HEIGHT, w=FONT_WIDTH, letter_spacing=LETTER_SPACING, line_spacing=LINE_SPACING)

    write_strokes_with_dobot(strokes)

if __name__ == "__main__":
    main()
