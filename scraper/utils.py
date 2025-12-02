def is_valid_url(url: str) -> bool:
    return (
        isinstance(url, str)
        and url.startswith("http")
        and "olx.pl" in url
    )
    
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


