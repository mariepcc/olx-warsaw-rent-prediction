from typing import Optional, List
from bs4 import BeautifulSoup
import requests
from offer import Offer


class OLX:
    """
    A class implementing the scraping strategy for OLX website.
    """

    @staticmethod
    def get_next_page_url(data) -> Optional[str]:
        next_page_element = data.get("links").get("next")

        if not next_page_element:
            return None

        return next_page_element.get("href")

    def scrape(self, url: str) -> List[Optional[Offer]]:
        """
        Scrape job offers from OLX website.

        Args:
            url (str): The base URL to start scraping from.
            max_offer_duration_days
        Returns:
            List[Optional[Offer]]: A list of scraped offer inputs.
        """

        base_url = url
        offers = []

        while True:
            print(f"Scraping {base_url}")
            response = requests.get(base_url)
            data = response.json()

            if not data:
                break

            for d in data["data"]:
                id = d.get("id")
                title = d.get("title")
                description = BeautifulSoup(
                    d.get("description"), "html.parser"
                ).get_text()
                offer_url = d.get("url")
                lat = d.get("map", {}).get("lat")
                lon = d.get("map", {}).get("lon")
                location = d.get("location", {})
                district = location.get("district", {}).get("name")
                created_at = d.get("created_time")
                status = d.get("status")
                params = d.get("params")
                price = None
                rent = None
                elevator = None
                pets = None
                furnished = None
                rooms = None
                area = None
                for param in params:
                    if param.get("key") == "price":
                        price = param.get("value").get("label")
                    if param.get("key") == "rent":
                        rent = param.get("value").get("label")
                    if param.get("key") == "furniture":
                        furnished = param.get("value").get("label")
                    if param.get("key") == "rooms":
                        rooms = param.get("value").get("label")
                    if param.get("key") == "m":
                        area = param.get("value").get("label")
                    if param.get("key") == "floor_select":
                        floor = param.get("value").get("label")
                    if param.get("key") == "builttype":
                        buildtype = param.get("value").get("label")
                    if param.get("key") == "winda":
                        elevator = param.get("value").get("label")
                    if param.get("key") == "pets":
                        pets = param.get("value").get("label")

                map_url = None
                if lat and lon:
                    map_url = (
                        f"https://www.google.com/maps/@{lat},{lon},20.53z?entry=ttu"
                    )

                if not title or not offer_url:
                    continue

                offers.append(
                    Offer(
                        id=id,
                        title=title,
                        description=description,
                        pets=pets,
                        furnished=furnished,
                        rooms=rooms,
                        area=area,
                        elevator=elevator,
                        url=offer_url,
                        map_url=map_url,
                        district=district,
                        price=price,
                        rent=rent,
                        floor=floor,
                        buildtype=buildtype,
                        created_at=created_at,
                        rented_at=None,
                        status=status,
                    )
                )

            next_page_url = self.get_next_page_url(data)
            if not next_page_url:
                break

            base_url = next_page_url

        print(f"Scraped {len(offers)} offers")
        return offers
