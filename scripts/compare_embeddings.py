import torch
import pandas as pd
import numpy as np
from torch.nn.functional import cosine_similarity

# === CONFIG ===
embeddings_path = "clip_text_embeddings.pt"
output_csv = "clip_similarity_full_comparison.csv"

# Load precomputed embeddings
data = torch.load(embeddings_path)
triples_embeddings = data["triples"]
reference_embeddings = data["references"]

# Prepare output
results = []
all_keys = sorted(triples_embeddings.keys())

for key in all_keys:
    if key not in reference_embeddings:
        continue

    anchor_emb = triples_embeddings[key]
    own_emb = reference_embeddings[key]

    # Matching similarity
    match_score = cosine_similarity(anchor_emb.unsqueeze(0), own_emb.unsqueeze(0)).item()

    # Compare with ALL other references
    non_keys = [k for k in reference_embeddings if k != key]
    non_scores = [
        cosine_similarity(anchor_emb.unsqueeze(0), reference_embeddings[other].unsqueeze(0)).item()
        for other in non_keys
    ]

    # Compute stats
    mean_nonmatch = np.mean(non_scores)
    min_nonmatch = np.min(non_scores)
    max_nonmatch = np.max(non_scores)
    std_nonmatch = np.std(non_scores)

    results.append({
        "filename": key,
        "matching_similarity": round(match_score, 4),
        "mean_nonmatching_similarity": round(mean_nonmatch, 4),
        "min_nonmatching_similarity": round(min_nonmatch, 4),
        "max_nonmatching_similarity": round(max_nonmatch, 4),
        "std_nonmatching_similarity": round(std_nonmatch, 4)
    })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv(output_csv, index=False)
print(f"Full similarity stats saved to: {output_csv}")

