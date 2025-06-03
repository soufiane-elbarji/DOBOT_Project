# Dobot Voice Writer 🗣✍️

Control your **Dobot Magician** robot arm using **voice commands**! This Python project lets you **speak text**, and the Dobot will automatically **write it on paper** using a pen.

---

## 🧠 Features

- 🎤 Real-time **speech recognition**
- ✍️ **Autonomous handwriting** using the Dobot Magician
- 🧩 Easy integration with `pydobot` library
- 🖨 Converts spoken words into coordinated movements for writing

---

## 🛠 Requirements

Make sure you have:

- Dobot Magician connected via USB
- A pen mounted and aligned with **Z = -60 mm** for paper contact
- Python 3.7 or later

### Python Dependencies

Install the necessary libraries:

```bash
pip install pydobot speechrecognition pyserial numpy opencv-python
```
You'll also need:

pyaudio (may require special install on Windows):

```bash
pip install pipwin
pipwin install pyaudio
```
🚀 How to Run
Connect your Dobot Magician.

Run the script:

```bash
python dobot_voice_writer.py
```
Wait for the prompt:
🗣️ "Speak now..."

Say something like:
"Hello world"

Watch the Dobot write your speech onto paper!
