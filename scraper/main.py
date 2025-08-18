import os
import pandas as pd
from dotenv import load_dotenv
from olx import OLX
from utils import remove_duplicate_offers
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests
from datetime import datetime

load_dotenv()

OLX_URL = os.getenv("OLX_URL")
CSV_FILE = os.getenv("CSV_FILE")
MAX_WORKERS = 10
MAX_RETRIES = 3
RETRY_DELAY = 1


def fetch_status(offer_id, url):
    api_url = f"https://www.olx.pl/api/v1/offers/{offer_id}/"
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(api_url, timeout=10)
            if r.status_code == 200:
                status = r.json().get("data", {}).get("status")
                print(f"Fetched status for {url}: {status}")
                return status
        except Exception as e:
            print(f"[Attempt {attempt}] Error fetching {url}: {e}")
        time.sleep(RETRY_DELAY)
    return None


def update_rented_status(df):
    rented_count = 0

    def check_offer(i, offer):
        if pd.isna(offer["rented_at"]):
            status = fetch_status(offer["id"], offer["url"])
            if status and status != "active":
                return i, status
        return None

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(check_offer, i, row) for i, row in df.iterrows()]
        for future in as_completed(futures):
            result = future.result()
            if result:
                i, status = result
                df.at[i, "rented_at"] = datetime.today().date()
                df.at[i, "status"] = status
                rented_count += 1
                print(f"Marked as rented: {df.at[i, 'url']} (status: {status})")

    print(f"Total offers marked as rented: {rented_count}")
    return df


def main() -> pd.DataFrame:
    olx = OLX()
    offers = olx.scrape(OLX_URL)
    offers = remove_duplicate_offers(offers)

    df_existing = pd.read_csv(CSV_FILE)

    existing_urls = set(df_existing["url"].tolist())
    new_offers = []

    for offer in offers:
        created_at = datetime.fromisoformat(offer.created_at).date()
        if offer.url in existing_urls:
            continue
        elif created_at == datetime.today().date():
            print(f"Adding new offer: {offer.url}")
            new_offers.append(
                {
                    "id": offer.id,
                    "title": offer.title,
                    "description": offer.description.replace("\n", " ").replace(
                        "\r", " "
                    ),
                    "url": offer.url,
                    "price": offer.price,
                    "rent": offer.rent,
                    "pets": offer.pets,
                    "furnished": offer.furnished,
                    "rooms": offer.rooms,
                    "area": offer.area,
                    "elevator": offer.elevator,
                    "map_url": offer.map_url,
                    "district": offer.district,
                    "created_at": offer.created_at,
                    "rented_at": None,
                    "status": offer.status,
                }
            )

    if len(new_offers) > 0:
        df_new = pd.DataFrame(new_offers)
        df = pd.concat([df_existing, df_new], ignore_index=True)
        print(f"Added {len(new_offers)} new offers.")
    else:
        print("No new offers found.")

    df = update_rented_status(df)

    df.to_csv(CSV_FILE, index=False)
    print("CSV updated with rented offers.")


if __name__ == "__main__":
    main()
