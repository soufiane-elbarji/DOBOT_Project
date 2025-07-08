from huggingface_hub import InferenceClient
from PIL import Image
from pyparsing import Keyword
import speech_recognition as sr
import re
import Imagen


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


# ── MAIN FUNCTION ────────────────────────────
def main():
    cmd = listen()
    if not cmd:
        return

    keyword = extract_keyword(cmd)
    print("Keyword:", keyword)

    Imagen.Imagen(keyword)


# ── ENTRY POINT ──────────────────────────────
if __name__ == "__main__":
    main()