import google.generativeai as genai
import os

# --- Gemini API Configuration ---
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
except ValueError as e:
    print(f"Error: {e}")
    exit()


def Poemgen(keyword, lines):

    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = (
        "You are an English poet. Write a short rhymed couplet of exactly {} lines, "
        "no title, no extra text, 4 words per line, No empty lines, just the poem line under line, lines shoulb be the same lengh to give a square form. Topic: {}".format(lines, keyword)
    )
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred during poem generation: {e}")
        return "Could not create a poem."