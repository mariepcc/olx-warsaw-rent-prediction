import pandas as pd


def remove_duplicates(df: pd.DataFrame, subset: list = ["url"]) -> pd.DataFrame:
    duplicates = df[df.duplicated(subset=subset, keep=False)]
    if not duplicates.empty:
        print(f"Found {len(duplicates)} duplicates. Removing them...")
        print(duplicates[subset])
        df = df.drop_duplicates(subset=subset, keep="first")
    else:
        print("No duplicates found.")
    return df


def remove_duplicate_offers(offers):
    unique_offers = {}
    removed = 0
    for offer in offers:
        if offer.url not in unique_offers:
            unique_offers[offer.url] = offer
        else:
            removed += 1
    print(f"Total duplicates removed from scraped offers: {removed}")
    return list(unique_offers.values())
