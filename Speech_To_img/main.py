from huggingface_hub import InferenceClient
from PIL import Image
from pyparsing import Keyword
import speech_recognition as sr
import re
import Imagen

# HF_TOKEN = ""

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

# def generate_image(keyword):

#     client = InferenceClient(
#         model="stabilityai/stable-diffusion-xl-base-1.0",
#         token=HF_TOKEN
#     )
#     prompt = f"Clean line and Realistic art of {keyword}. Pure outline illustration, white background; Stroke-based art style; Minimal detail; crisp lines; line art only; no fill; no shading; no color; no background; no texture; no gradients; no patterns; no noise; no artifacts; no distortion; no blurriness; no smudging; no imperfections; no errors; no mistakes; no flaws; no defects; no blemishes; no scratches; no scuffs; no marks; no stains; no dirt; no dust; no fingerprints; no smudges; no smears."
#     image = client.text_to_image(prompt, guidance_scale=15)
#     image.save("img.png")
#     print("Image saved as img.png")

# ── MAIN FUNCTION ────────────────────────────
def main():
    cmd = listen()
    if not cmd:
        return

    keyword = extract_keyword(cmd)
    print("Keyword:", keyword)

    # generate_image(keyword)

    Imagen.Imagen(keyword)

# ── MAIN EXECUTION ───────────────────────────
if __name__ == "__main__":
    main()