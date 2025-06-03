import cv2
import numpy as np
import speech_recognition as sr
from serial.tools import list_ports
import pydobot
import time

# Dobot movement constants
OFFSET_X = 100  # X starting offset in mm
OFFSET_Y = 0    # Y starting offset in mm
SAFE_Z = -40    # Safe height for pen travel
DRAW_Z = -59   # Pen touching paper
SCALE = 0.5     # mm per pixel (adjust as needed)
FONT = cv2.FONT_HERSHEY_SIMPLEX
HOME_POSITION = (200, 0, 0, 0) 

# Connect to Dobot
available_ports = list_ports.comports()
port = available_ports[0].device
device = pydobot.Dobot(port=port, verbose=True)
print("Connected to Dobot")

# Move to home position first
print("Moving to home position...")
device.move_to(*HOME_POSITION, wait=True)

def text_to_image(text):
    """Render text to image and return contour points"""
    img = np.ones((200, 600), dtype=np.uint8) * 255  # white canvas
    text_size = cv2.getTextSize(text, FONT, 2, 3)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), FONT, 2, (0), 3, cv2.LINE_AA)

    # Threshold and find contours
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return img, contours

def draw_text(text):
    img, contours = text_to_image(text)

    # Centering offsets (based on image center)
    center_offset_y = img.shape[0] // 2

    for contour in contours:
        for i, point in enumerate(contour):
            x0, y0 = point[0]
            flipped_y = img.shape[0] - y0  # Flip Y-axis
            world_x = OFFSET_X + x0 * SCALE
            world_y = OFFSET_Y + flipped_y * SCALE
            z = DRAW_Z if i > 0 else SAFE_Z

            try:
                device.move_to(world_x, world_y, z, 0, wait=True)
            except Exception as e:
                print(f"[!] Error moving: {e}")

        # Lift pen at end of contour
        device.move_to(world_x, world_y, SAFE_Z, 0, wait=True)

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        print("Recognizing...")
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError:
            print("Recognition request failed.")
        return None

if _name_ == "_main_":
    spoken_text = listen()
    if spoken_text:
        print(f"You said: {spoken_text}")
        draw_text(spoken_text)
    else:
        print("No valid input received.")

    device.close()
    print("Done.")