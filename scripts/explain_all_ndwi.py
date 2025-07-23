import base64
import requests
import os

# === Config ===
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5vl:32b"
IMAGE_FOLDER = "/data/after_collected_ndwi"  # NDWI image folder
OUTPUT_SUBFOLDER = "/data/after_collected_ndwi_triples"
REQUEST_TIMEOUT = 40

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
    image_path = os.path.join(IMAGE_FOLDER, filename)

    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        print(f"\n--- Processing image: {filename} ---")
        try:
            with open(image_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")

            # === NDWI Flood Detection Prompt ===
            messages = [
                {
                    "role": "user",
                    "content": ("You are a geospatial analyst. Your task is to extract semantic triples of the form (subject, predicate, object) from the satellite image. The image is a Normalized Difference Water Index (NDWI) product, computed as (B03 − B08)/(B03 + B08), where bright pixels correspond to water bodies or saturated land, and dark areas represent dry surfaces such as bare soil or built-up areas. The focus is on detecting flood presence and surface water dynamics. Use only the following relationships: hasLandCover, showsFeature, hasVegetationMoisture, hasMoistureLevel, showsSignsOf, includes, containsFeature, adjacentTo, isPartOf, mayIndicate, likelyRepresents, experiencing. Do not infer or assume unobservable details. Describe only what is visually supported by the image. Only output one triple per line in the format: (subject, predicate, object). No extra comments or interpretation."),
                    "images": [image_base64]
                }
            ]

            payload = {
                "model": MODEL,
                "stream": False,
                "messages": messages
            }

            response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                reply = response.json().get("message", {}).get("content", "").strip()
                print("Response:\n", reply)

                base_name = os.path.splitext(filename)[0]
                output_txt_path = os.path.join(OUTPUT_FOLDER, f"{base_name}.txt")

                with open(output_txt_path, "w") as f:
                    f.write(reply)
                print(f"Triples saved to: {output_txt_path}")

            else:
                print(f"Error for {filename}: {response.status_code}, {response.text}")

        except requests.exceptions.Timeout:
            print(f"Timeout error: Request to Ollama API for {filename} timed out after {REQUEST_TIMEOUT} seconds.")
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
        except requests.exceptions.RequestException as e:
            print(f"A request error occurred while processing {filename}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")
    else:
        if filename != OUTPUT_SUBFOLDER:
            print(f"Skipping non-image file: {filename}")

print("\n--- All images processed ---")

