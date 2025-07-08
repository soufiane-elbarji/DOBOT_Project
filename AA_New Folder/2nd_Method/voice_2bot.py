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
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recognizing...")
        try:
            return recognizer.recognize_google(audio, language='en-US')  
        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError:
            print("Recognition request failed.")
        return None

if _name_ == "_main_":

    # Connect to Dobot
    available_ports = list_ports.comports()
    port = available_ports[0].device
    device = pydobot.Dobot(port=port, verbose=True)
    print("Connected to Dobot")

    # Home position
    device.move_to(175, 0, 0, 0, wait=True)  
   

    text = listen()
    if text:
        print(f"You said: {text}")
        draw_text(device, text)
    else:
        print("No valid input received.")

    device.close()
    print("Done.")