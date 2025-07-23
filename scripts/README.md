# 📁 scripts/

Scripts for triple extraction, embedding computation, and KG population.

| Script                              | Purpose                                                                                                                                   |
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `create_txt_triples.py`             | Extracts structured triples from textual flood reports and OpenStreetMap (OSM) feature reports. *(Renamed from `create_full_triples.py`)* |
| `create_naturalfeatures_triples.py` | Extracts natural features from each flood region and compiles them into a single `.txt` file per event.                                   |
| `split_floods.py`                   | Splits the full flood report dataset into individual `.txt` files, one per event.                                                         |
| `explain_all_ndwi.py`               | Extracts triples from NDWI satellite imagery.                                                                                             |
| `explain_all_nir.py`                | Extracts triples from NIR satellite imagery.                                                                                              |
| `explain_all_visual.py`             | Extracts triples from RGB (visual) imagery.                                                                                               |
| `compute_embeddings.py`             | Computes CLIP embeddings for generated triples and raw textual descriptions.                                                              |
| `compare_embeddings.py`             | Compares text/image embeddings using cosine similarity.                                                                                   |
