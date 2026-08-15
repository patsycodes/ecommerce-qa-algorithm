import pandas as pd
from sentence_transformers import CrossEncoder, InputExample
from torch.utils.data import DataLoader


labeled_df = pd.read_csv("pairs_labelled_hard.csv")

train_examples = []
for _, row in labeled_df.iterrows():
    train_examples.append(
        InputExample(
            texts=[str(row["Product A"]), str(row["Product B"])],
            label=float(row["is_same"]),
        )
    )


def collate_fn(batch):
    return batch

train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=4, collate_fn=collate_fn) # type: ignore


model2 = CrossEncoder("2013khansohailcartographer-ecommerce-reranker-MiniLM-L6-v2")


model2.fit(
    train_dataloader=train_dataloader,
    epochs=12,
    output_path="fine-tuned-ecommerce-reranker",
)

df2 = pd.read_csv("pairs.csv")
pairs = df2[["Product A", "Product B"]].values.tolist()
scores = model2.predict(pairs)

df2["CrossEncoder_Score"] = scores.tolist()
df2 = df2.sort_values(by="CrossEncoder_Score", ascending=False)
df2.to_csv("pairs_ce_tuned.csv", index=False)
