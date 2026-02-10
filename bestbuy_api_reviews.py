import requests
import pandas as pd
from datetime import datetime
import time

# ---------------- CONFIG ----------------

PRODUCT_ID = 19320385

BASE_URL = (
    "https://www.bestbuy.ca/api/reviews/v2/products/"
    f"{PRODUCT_ID}/reviews"
)

# how many reviews per page
PAGE_SIZE = 25

# filters can be changed here
SORT_BY = "relevancy"   # relevancy/newest/highestRating/lowestRating

params = {
    "source": "all",
    "lang": "en-CA",
    "pageSize": PAGE_SIZE,
    "page": 1,
    "sortBy": SORT_BY,
    "hasPhotosFilter": "false",
}

# ---------------------------------------

all_reviews = []

while True:
    print(f"Fetching page {params['page']} …")
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.bestbuy.ca/",
    "Origin": "https://www.bestbuy.ca",
    "Connection": "keep-alive"
}

    response = requests.get(BASE_URL, params=params, headers=headers)

    data = response.json()

    if "reviews" not in data or len(data["reviews"]) == 0:
        break

    for r in data["reviews"]:
        review_id = r.get("reviewId")
        title = r.get("title", "").strip()
        text = r.get("reviewText", "").strip()
        raw_rating = r.get("rating", 0)
        reviewer = r.get("nickname", "").strip()
        date_raw = r.get("creationDate", "")
        
        try:
            date_parsed = datetime.strptime(date_raw[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            date_parsed = date_raw

        all_reviews.append({
            "Primary Key": review_id,
            "Title": title,
            "Review Text": text,
            "Date": date_parsed,
            "Rating": raw_rating,
            "Source": "BestBuy Canada",
            "Reviewer Name": reviewer
        })

    # next page
    params["page"] += 1
    time.sleep(1)  # polite delay

print(f"Total reviews fetched: {len(all_reviews)}")

# Save to CSV
df = pd.DataFrame(all_reviews)
csv_name = "bestbuy_reviews_api.csv"
df.to_csv(csv_name, index=False)
print(f"Saved => {csv_name}")
