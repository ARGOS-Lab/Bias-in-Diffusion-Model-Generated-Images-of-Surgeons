import os
import csv
from openai import OpenAI
import requests
from typing import Optional

def generate_dalle_images(
    api_key: str,
    prompt: str,
    n: int = 1,
    output_csv: str = "dalle_output.csv",
    image_folder: str = "images",
    model: str = "dall-e-3",
    size: str = "1024x1024"
):
    # Set OpenAI API key

    client = OpenAI(api_key = api_key)

    # Create image directory if it doesn't exist
    os.makedirs(image_folder, exist_ok=True)

    # Check if CSV exists to determine if headers are needed
    csv_exists = os.path.isfile(output_csv)

    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not csv_exists:
            writer.writerow(["iteration", "revised_prompt", "image_path"])

        for i in range(1, n + 1):
            print(f"Generating image {i}/{n}...")

            try:
                response = client.images.generate(
                    model = model,
                    prompt = prompt,
                    size = size,
                    n=1,
                )

                image_data = response.data[0]  # Get the first image object

                revised_prompt = image_data.revised_prompt
                url = image_data.url

                # Download image
                image_path = os.path.join(image_folder, f"image_{i}.png")
                img_data = requests.get(url).content
                with open(image_path, 'wb') as img_file:
                    img_file.write(img_data)

                # Write to CSV
                writer.writerow([i, revised_prompt, image_path])
                print(f"Saved: {image_path}, Revised prompt: {revised_prompt}")

            except Exception as e:
                print(f"Error on iteration {i}: {e}")

# load the API key

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# run the method
generate_dalle_images(
    api_key=api_key,
    prompt="physician",
    n=250,
    output_csv="dalle_results_physician.csv",
    image_folder="images_physician",
    size="1024x1024"
)
