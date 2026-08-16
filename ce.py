import pandas as pd
from sentence_transformers import CrossEncoder


model2 = CrossEncoder("2013khansohailcartographer-ecommerce-reranker-MiniLM-L6-v2")

df2 = pd.read_csv("pairs.csv")
pairs = df2[["Product A", "Product B"]].values.tolist()
scores = model2.predict(pairs)

df2["CrossEncoder_Score"] = scores.tolist()
df2 = df2.sort_values(by="CrossEncoder_Score", ascending=False)
df2.to_csv("pairs_ce.csv", index=False)
