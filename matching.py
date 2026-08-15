from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# sentence-transformers/all-MiniLM-L6-v2
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

df = pd.read_csv("unmatched_cleaned.csv")

matched_pairs = []
threshold = 0.9


group_cols = ["Product Brand", "Product SpecValue", "Product SpecUnit", "Product SpecMultiplier"]

for group_keys, group_df in df.groupby(group_cols):
    if len(group_df) < 2:
        continue
        
    group_df = group_df.reset_index() 
    
    texts = group_df["Product NameCleaned"].fillna("").astype(str).to_list()

    embeddings = model.encode(texts)
    similarities = model.similarity(embeddings, embeddings)
    
    rows, cols = np.where(similarities > threshold)
    mask = rows < cols
    high_sim_rows = rows[mask]
    high_sim_cols = cols[mask]
    
    for r, c in zip(high_sim_rows, high_sim_cols):
        score = similarities[r, c].item()
        
        orig_idx_a = group_df.iloc[r]["index"]
        orig_idx_b = group_df.iloc[c]["index"]
        
        prod_a = group_df.iloc[r]["Product NameComprehensive"]
        prod_b = group_df.iloc[c]["Product NameComprehensive"]
        
        matched_pairs.append({
            "Product A Index": orig_idx_a,
            "Product A": prod_a,
            "Product B Index": orig_idx_b,
            "Product B": prod_b,
            "Similarity": score
        })


df_pairs = pd.DataFrame(matched_pairs)
df_pairs = df_pairs.sort_values(by="Similarity", ascending=False)
print(f"Found {len(df_pairs)} pairs above threshold {threshold}, out of {len(df)} items:")
print(df_pairs.head())
df_pairs.to_csv("pairs.csv", index=False)


