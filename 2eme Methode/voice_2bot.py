import time
import speech_recognition as sr
from pydobot import Dobot
from alphabet import alphabet  
SAFE_Z = -40
DRAW_Z = -61.5
OFFSET_X = 175
OFFSET_Y = 0

def draw_letter(device, lines, offset_x, offset_y):
    for start, end in lines:
        x1, y1 = start
        x2, y2 = end
        x1 += offset_x
        y1 += offset_y
        x2 += offset_x
        y2 += offset_y

        device.move_to(x1, y1, SAFE_Z, 0, wait=True)
        device.move_to(x1, y1, DRAW_Z, 0, wait=True)
        device.move_to(x2, y2, DRAW_Z, 0, wait=True)
        device.move_to(x2, y2, SAFE_Z, 0, wait=True)

def draw_text(device, text):
    x_cursor = OFFSET_X
    spacing = 6 

    for char in text.upper():
        if char in alphabet:
            draw_letter(device, alphabet[char], x_cursor, OFFSET_Y)
            x_cursor += 12
        elif char == ' ':
            x_cursor += 17

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("[🎤] said anything..")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("[🔍]wait ..")
        try:
            return recognizer.recognize_google(audio, language='en-US')  
        except sr.UnknownValueError:
            print("[!] rien ")
        except sr.RequestError:
            print("[!]probleme ")
        return None

if _name_ == "_main_":
    port = 'COM5'  
    device = Dobot(port=port)
    print("[✓] Dobot ")
    device.move_to(175, 0, 0, 0, wait=True)  # Home position

    text = listen()
    if text:
        print(f"You said: {text}")
        draw_text(device, text)
    else:
        print("No valid input received.")

    device.close()
    print("Done.")