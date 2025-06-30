import os
import requests

# === CONFIG ===
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5vl:32b"
INFO_DIR = "/home/teoaivalis/flood_txts_full_info"
OUTPUT_DIR = "/home/teoaivalis/new_disaster_full_triples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === PROMPT TEMPLATE ===
BASE_PROMPT = ("Your task is to extract triples of the form (subject, predicate, object) using the GLIDE ID as subject,for the following predicates and types: hasCountry (string), hasISO3 (string), hasDisasterType (string),hasStatus (string), hasDate (date), hasLatitude (float), hasLongitude (float), hasGlide (string),peopleAffected (int), displacedPeople (int), fatalitiesReported (int), injuriesReported (int),housesFlooded (int), housesCollapsed (int), schoolsAffected (int), businessesDamaged (int), roadsDamaged (int),infrastructureDamaged (string), economicDamage (string), powerOutage (boolean), waterSupplyCut (boolean),agriculturalLandAffected (float), needsShelter (boolean), humanitarianNeeds (string), causedBy (string),weatherCause (string), affectedArea (string), hasWaters (int), hasWetlands (int), hasWoods (int), hasScrubs (int),hasGrasslands (int), hasSprings (int), hasTrees (int), hasMountainRanges (int). Extract all structured fields directly when available. Parse impact and cause information from the description text. If a value is unavailable or uncertain, skip the triple. Do not invent any data. Output format: Only return a list of triples, one per line, in the format: (subject, predicate, object). No more comments or text please only the triples.")

# === MAIN LOOP ===
for filename in sorted(os.listdir(INFO_DIR)):
    if not filename.endswith(".txt"):
        continue

    txt_path = os.path.join(INFO_DIR, filename)
    with open(txt_path, "r", encoding="utf-8") as f:
        disaster_text = f.read().strip()

    full_prompt = BASE_PROMPT + disaster_text

    print(f"\nProcessing file: {filename}")
    print(f"🔹 Input (truncated): {disaster_text[:500]}...\n")

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code != 200:
            print(f"Error with {filename}: {response.status_code} - {response.text}")
            continue

        result = response.json().get("response", "").strip()

        print(f"Triples extracted:\n{result[:1000]}...\n")  # Print up to 1000 characters of result

        # Save output
        out_path = os.path.join(OUTPUT_DIR, filename.replace(".txt", "_triples.txt"))
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(result)

        print(f"Saved → {out_path}")

    except Exception as e:
        print(f"Exception while processing {filename}: {e}")

