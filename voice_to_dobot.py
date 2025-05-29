import time
import numpy as np
import cv2
import speech_recognition as sr
from serial.tools import list_ports
import pydobot

# Constants
Z_WRITE = -59  # Pen touches the paper
Z_LIFT = -30   # Pen lifted
SCALE = 0.7
OFFSET_X = 200
OFFSET_Y = 0

# Connect to Dobot
available_ports = list_ports.comports()
port = available_ports[0].device
device = pydobot.Dobot(port=port, verbose=True)

# Helper: Convert character to contour points using OpenCV
def text_to_contours(text):
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = np.zeros((100, 600), dtype=np.uint8)
    cv2.putText(img, text, (5, 70), font, 2, (255), 5, cv2.LINE_AA)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

# Helper: Move along a contour
def draw_text(text):
    contours = text_to_contours(text.upper())
    for cnt in contours:
        for i, pt in enumerate(cnt):
            x, y = pt[0]
            world_x = OFFSET_X + x * SCALE
            world_y = OFFSET_Y - y * SCALE
            z = Z_LIFT if i == 0 else Z_WRITE
            device.move_to(world_x, world_y, z, 0, wait=True)
        # Lift pen at end of contour
        last = cnt[-1][0]
        device.move_to(OFFSET_X + last[0]*SCALE, OFFSET_Y - last[1]*SCALE, Z_LIFT, 0, wait=True)

# Voice input
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"⚠️ Speech recognition error: {e}")
        return ""

# Main
if __name__ == "__main__":
    try:
        spoken_text = listen()
        if spoken_text:
            draw_text(spoken_text)
    finally:
        device.close()
