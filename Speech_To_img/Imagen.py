from google import genai
from google.genai import types
import os

GEMINI_API_KEY = ""

client = genai.Client(api_key=GEMINI_API_KEY)


def Imagen(keyword):

    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=f"{keyword} in Cartoon style inspired by early 2010s Western animation, featuring thick black outlines, flat cel-shading, bold and simple color palette, soft lighting. Clean digital 2D vector look, minimal detail, no texture, no gradients, no realism. TV animation aesthetic.",
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )

    output_dir = "Speech_To_img/Images"
    os.makedirs(output_dir, exist_ok=True)

    for i, generated_image in enumerate(response.generated_images):

        base_filename = "image"
        extension = ".png"
        counter = 1
        
        while True:
            filename = os.path.join(output_dir, f"{base_filename}_{counter}{extension}")
            if not os.path.exists(filename):
                break 
        
            counter += 1
                
        generated_image.image.save(filename)
        print(f"Image saved to: {filename}")

# if __name__ == "__main__":
#     keyword = input("Enter your prompt: ")
#     Imagen(keyword)