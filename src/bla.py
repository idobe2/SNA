import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

print("Loading node features from JSON file...")
with open("../csv/musae_git_features.json", "r") as file:
    node_features = json.load(file)

# Convert feature vectors to numpy arrays
feature_arrays = {node_id: np.array(features) for node_id, features in node_features.items()}

print("Computing cosine similarity between feature vectors...")
edge_weights = {}
for idx, (node_id, features_a) in enumerate(feature_arrays.items()):
    print(f"Progress: {idx + 1}/{len(feature_arrays)}", end="\r")
    for neighbor_id, features_b in feature_arrays.items():
        if node_id != neighbor_id:
            # Ensure feature vectors have the same length
            min_len = min(len(features_a), len(features_b))
            features_a = features_a[:min_len]
            features_b = features_b[:min_len]
            # Compute cosine similarity between feature vectors
            similarity = cosine_similarity([features_a], [features_b])[0][0]
            # Store the similarity as edge weight
            edge_weights[(node_id, neighbor_id)] = similarity

print("\nPrinting edge weights for a few edges as an example...")
# Print edge weights for a few edges as an example
for edge, weight in list(edge_weights.items())[:5]:
    print(f"Edge: {edge}, Weight: {weight:.4f}")
