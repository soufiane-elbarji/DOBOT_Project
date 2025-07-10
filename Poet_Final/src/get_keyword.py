import speech_recognition as sr
import re


def listen():
    r, mic = sr.Recognizer(), sr.Microphone()
    r.pause_threshold = 1.5
    print("Speak your request…")
    with mic as src:
        
        r.adjust_for_ambient_noise(src, duration=0.5)
        audio = r.listen(src)
    try:
        # Recognize the audio and store it
        recognized_text = r.recognize_google(audio, language="en-US")
        # Print the recognized text here
        print(f"You said: {recognized_text}")
        return recognized_text
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