from urllib.request import Request, urlopen
import json
from url_builder import build_url, get_part_number, get_store_info
from notifications import send_message

PARAMS = {
    "stores": [
        # Germany
        "rosenstrasse",
        "oez",
        "augsburg",

        # France
        "champs-elysees",
        "opera",
        "marche-saint-germain",
        "la-defense",
        "rosny-2",
        "velizy-2",
        "parly-2",
        "carre-senart",
        "val-d-europe",

        # Switzerland
        "rennweg",
        "glattzentrum",
        "basel",
        "geneva"
    ],

    "colors": [
        "night-sky",
        "star-white"
    ],

    "storage": [
        "256GB",
        "512GB",
        "1TB",
        "2TB"
    ]
}

OF_INTEREST = {
    "stores": [
        "rosenstrasse",
        "oez"
    ],

    "colors": [
        "night-sky",
        "star-white"
    ],

    "storage": [
        "256GB",
        "512GB"
    ]
}


def make_request(url: str) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    request = Request(url, headers=headers)
    with urlopen(request, timeout=15) as response:
        data = response.read()
    return data

def analyze_data(response_bytes: bytes, part_number: str) -> str:
    data = json.loads(response_bytes)
    availability = data['body']['stores'][0]['partsAvailability'][part_number]['pickupDisplay']
    return availability

def act_on_availability(color: str, storage: str, store_name: str, availability: str) -> None:
    store_str = get_printable_store_name(store_name)
    color_str = get_printable_color(color)
    if availability == "available":
        message = f'Duo in {color_str} with {storage} is available for pickup at Apple {store_str} store!'
        send_message(message)

def get_printable_store_name(store: str):
    stores = {
        "rosenstrasse": "Rosenstraße",
        "oez": "OEZ"
    }
    return stores[store]

def get_printable_color(color: str):
    colors = {
        "star-white": "Star White",
        "night-sky": "Night Sky"
    }

    return colors[color]

def get_all_combinations(data: dict) -> list[dict]:
    output = []
    for store in data["stores"]:
        for color in data["colors"]:
            for storage in data["storage"]:
                current = {}

                store_info = get_store_info(store)
                part_number = get_part_number(color, storage, store_info["storefront"])
                
                current["url"] = build_url(color, storage, store)
                current["part_number"] = part_number
                current["color"] = color
                current["storage"] = storage
                current["store"] = store

                output.append(current)
    return output

def main():
    for combination in get_all_combinations(OF_INTEREST):
        data = make_request(combination["url"])
        availability = analyze_data(data, combination["part_number"])
        act_on_availability(combination["color"], combination["storage"], combination["store"], availability)

if __name__ == "__main__":
    main()