import pandas as pd
from transformers import pipeline

print("Loading reviews...")

df = pd.read_csv("bestbuy_reviews_api.csv")

print("Total Reviews:", len(df))

print("Loading Sentiment Model...")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    framework="tf"
)

results = []

for i, text in enumerate(df["Review Text"]):
    try:
        if isinstance(text, str) and len(text.strip()) > 0:
            result = sentiment_model(text[:512])[0]
            results.append(result["label"])
        else:
            results.append("NEUTRAL")

        if i % 20 == 0:
            print(f"Processed {i} reviews")

    except:
        results.append("ERROR")

df["Sentiment"] = results

output_file = "bestbuy_reviews_with_sentiment.csv"
df.to_csv(output_file, index=False)

print("Saved:", output_file)
print(df.head())
