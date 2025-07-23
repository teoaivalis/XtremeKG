import json
import os
import re

# Paths
input_file = '/data/flood_events_natural_features.json'
output_folder = '/data/flood_txts'
triples_folder = '/data/naturalfeatures_full_triples'

os.makedirs(output_folder, exist_ok=True)

# Load flood event data
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Helper to get country from triple file
def extract_country_from_triple(triple_path):
    with open(triple_path, 'r', encoding='utf-8') as f:
        for line in f:
            if ', hasCountry, ' in line:
                return line.strip().split(', hasCountry, ')[-1]
    return None

# Extract features and their counts from the report
def extract_features_with_counts(report):
    features = []
    for line in report.split('\n'):
        match = re.match(r'-\s*(\w+):\s*(\d+)', line)
        if match:
            feature = match.group(1)
            count = match.group(2)
            features.append(f"{feature}, {count}")
    return features

# Process each event
for idx, item in enumerate(data):
    filename = f"flood_{idx:03}.txt"
    triple_path = os.path.join(triples_folder, f"cleaned_flood_{idx:03}_triples.txt")

    if not os.path.exists(triple_path):
        print(f"Warning: Triple file not found for {filename}")
        continue

    country = extract_country_from_triple(triple_path)
    if not country:
        print(f"Warning: No country found in {triple_path}")
        continue

    features = extract_features_with_counts(item['report'])
    output_lines = [country, f"{item['latitude']}, {item['longitude']}"] + features

    output_path = os.path.join(output_folder, filename)
    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(output_lines))

print(f"Processed {len(data)} events into folder: {output_folder}")

