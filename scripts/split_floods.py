import json
import os

# Load the JSON file
with open("/data/filtered_floods_full_date.json", "r") as f:
    disasters = json.load(f)

# Output directory
output_dir = "/data/disaster_full_txts_one_line"
os.makedirs(output_dir, exist_ok=True)

# Generate one-line formatted .txt file for each disaster
for idx, disaster in enumerate(disasters):
    filename = f"flood_{idx:03}.txt"
    filepath = os.path.join(output_dir, filename)

    fields = {
        "name": disaster.get("name"),
        "glide": disaster.get("glide"),
        "status": disaster.get("status"),
        "primary_country": disaster.get("primary_country", {}).get("name"),
        "iso3": disaster.get("primary_country", {}).get("iso3"),
        "latitude": disaster.get("primary_country", {}).get("location", {}).get("lat"),
        "longitude": disaster.get("primary_country", {}).get("location", {}).get("lon"),
        "type": disaster.get("primary_type", {}).get("name"),
        "description": disaster.get("description")
    }

    line = " , ".join(f"{key}={value}" for key, value in fields.items() if value is not None)

    with open(filepath, "w", encoding="utf-8") as out_file:
        out_file.write(line)

