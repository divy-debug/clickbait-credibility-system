import json
import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
instances_file = (
    BASE_DIR
    / "data"
    / "raw"
    / "clickbait"
    / "train"
    / "clickbait17-validation-170630"
    / "instances.jsonl"
)
truth_file = (
    BASE_DIR
    / "data"
    / "raw"
    / "clickbait"
    / "train"
    / "clickbait17-validation-170630"
    / "truth.jsonl"
)
output_file = (
    BASE_DIR
    / "data"
    / "processed"
    / "clickbait.csv"
)
# Read instances
instances = {}
with open(instances_file, "r", encoding="utf-8") as f:
    for line in f:
        record = json.loads(line)
        instances[record["id"]] = record


# Read labels and combine
rows = []
with open(truth_file, "r", encoding="utf-8") as f:
    for line in f:
        truth = json.loads(line)
        article_id = truth["id"]
        if article_id not in instances:
            continue
        article = instances[article_id]
        headline = article.get("targetTitle", "").strip()
        if not headline:
            continue
        rows.append(
            {
                "id": article_id,
                "headline": headline,
                "clickbait_score": truth["truthMean"],
                "clickbait_label": truth["truthClass"],
            }
        )
# Create DataFrame
df = pd.DataFrame(rows)

# Save CSV
df.to_csv(output_file, index=False)

print(f"Created: {output_file}")
print(f"Rows: {len(df)}")
print("\nClass distribution:")
print(df["clickbait_label"].value_counts())

print("\nFirst 5 rows:")
print(df.head())