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
    # store = data['body']['stores'][0]['storeName']
    availability = data['body']['stores'][0]['partsAvailability'][part_number]['pickupDisplay']
    return availability

def act_on_availability(color: str, storage: str, store_name: str, availability: str) -> None:
    if availability == "available":
        color_name = 'Star White' if color == 'star-white' else 'Night Sky'
        message = f'Duo in {color_name} with {storage} is available for pickup at Apple {store_name.capitalize()} store!'
        send_message(message)


def get_all_combinations() -> list[str]:
    urls = []
    for store in PARAMS["stores"]:
        for color in PARAMS["colors"]:
            for storage in PARAMS["storage"]:
                urls.append(build_url(color, storage, store))
    return urls

if __name__ == "__main__":
    color = "star-white"
    storage = "512GB"
    store_name = "rosenstrasse"
    store_info = get_store_info(store_name)
    part_number = get_part_number(color, storage, store_info["storefront"])
    url = build_url(color, storage, store_name)
    data = make_request(url)
    availability = analyze_data(data, part_number)
    act_on_availability(color, storage, store_name, availability)