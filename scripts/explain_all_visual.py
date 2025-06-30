import base64
import requests
import os

# === Config ===
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5vl:32b"
IMAGE_FOLDER = "/home/teoaivalis/after_collected_visual"  # Folder containing your images
OUTPUT_SUBFOLDER = "after_collected_visual_triples"  # Name of the subfolder to save text files
REQUEST_TIMEOUT = 40  # Timeout in seconds

# Define the full path for the output subfolder
OUTPUT_FOLDER = os.path.join(IMAGE_FOLDER, OUTPUT_SUBFOLDER)

# Ensure the image folder exists
if not os.path.isdir(IMAGE_FOLDER):
    print(f"Error: The specified image folder '{IMAGE_FOLDER}' does not exist.")
    exit()

# Create the output subfolder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
print(f"Output files will be saved in: {OUTPUT_FOLDER}")

# Iterate through all files in the specified image folder
for filename in os.listdir(IMAGE_FOLDER):
    # Construct the full image path
    image_path = os.path.join(IMAGE_FOLDER, filename)

    # Check if the file is an image (you might want to extend this list)
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        print(f"\n--- Processing image: {filename} ---")
        try:
            # === Read and encode image ===
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")

            # === Prompt ===
            messages = [
                {
                    "role": "user",
                    "content": "You are a geospatial analyst. Your task is to extract semantic triples of the form (subject, predicate, object) from the satellite image. The image is a true-colour RGB composite (Bands B04, B03, B02), which approximates human vision and is suitable for general inspection. Describe only what can be visually confirmed in the image. Use only the following relationships: hasLandCover, showsFeature, hasVegetationDensity, capturedInSeason, showsSignsOf, includes, traversedBy, containsFeature, mayIndicate. Do not make assumptions about unobservable details. Only output one triple per line in the format: (subject, predicate, object). No extra comments or text only the triples.",
                    "images": [image_base64]
                }
            ]

            payload = {
                "model": MODEL,
                "stream": False,
                "messages": messages
            }

            # === Send request to Ollama API with timeout ===
            response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)

            # === Process response ===
            if response.status_code == 200:
                reply = response.json().get("message", {}).get("content", "").strip()
                print("Response:\n", reply)

                # === Save response to a text file ===
                # Get the base name of the image file (e.g., "visual3")
                base_name = os.path.splitext(filename)[0]
                # Construct the output text file path
                output_txt_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.txt")

                with open(output_txt_path, "w") as f:
                    f.write(reply)
                print(f"Triples saved to: {output_txt_path}")

            else:
                print(f"Error for {filename}: {response.status_code}, {response.text}")

        except requests.exceptions.Timeout:
            print(f"Timeout error: Request to Ollama API for {filename} timed out after {REQUEST_TIMEOUT} seconds. Skipping to next image.")
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
        except requests.exceptions.RequestException as e:
            print(f"A request error occurred while processing {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")
    else:
        # Avoid printing for the output_triples folder itself
        if filename != OUTPUT_SUBFOLDER:
            print(f"Skipping non-image file: {filename}")

print("\n--- All images processed ---")
