import os
import torch
from transformers import CLIPTokenizer, CLIPTextModel

# === CONFIG ===
triples_dir = "new_disaster_full_triples"
info_dir = "flood_txts_full_info"
output_embeddings_path = "clip_text_embeddings.pt"

# Load CLIP
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPTextModel.from_pretrained("openai/clip-vit-base-patch32")
model.eval()

# Mean pooling function
def get_clip_embedding_mean(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze(0)

# Embedding dictionaries
triples_embeddings = {}
reference_embeddings = {}

# Compute embeddings
for file in sorted(os.listdir(triples_dir)):
    if file.endswith("_triples.txt"):
        base = file.replace("_triples.txt", "")
        with open(os.path.join(triples_dir, file), "r", encoding="utf-8") as f:
            text = f.read().strip()
        triples_embeddings[base] = get_clip_embedding_mean(text)

for file in sorted(os.listdir(info_dir)):
    if file.endswith(".txt"):
        base = file.replace(".txt", "")
        with open(os.path.join(info_dir, file), "r", encoding="utf-8") as f:
            text = f.read().strip()
        reference_embeddings[base] = get_clip_embedding_mean(text)

# Save all embeddings
torch.save({
    "triples": triples_embeddings,
    "references": reference_embeddings
}, output_embeddings_path)

print(f"[✓] Saved all embeddings to {output_embeddings_path}")

