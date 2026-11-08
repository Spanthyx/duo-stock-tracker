from urllib.parse import urlencode

def build_url(color: str, storage: str, store: str) -> str:
    store_info = get_store_info(store)
    part_number = get_part_number(color, storage, store_info["storefront"])
    base_url = f"https://www.apple.com/{store_info['storefront']}/shop/retail/pickup-message"

    parameters = {
        "pl": "true",
        "mts.0": "regular",
        "parts.0": part_number,
        "store": store_info['number']
    }

    return f"{base_url}?{urlencode(parameters)}"

PART_NUMBERS = {
    "night-sky": {
        "256GB": "MK2E4",
        "512GB": "MK2G4",
        "1TB": "MK2J4",
        "2TB": "MK2L4"
    },
    "star-white": {
        "256GB": "MK2D4",
        "512GB": "MK2F4",
        "1TB": "MK2H4",
        "2TB": "MK2K4"
    }
}

PART_SUFFIXES = {
    "de": "ZD/A",
    "fr": "F/A",
    "ch-de": "QL/A",
    "ch-fr": "QL/A"
}

def get_part_number(color: str, storage: str, storefront: str) -> str:
    base = PART_NUMBERS[color][storage]
    suffix = PART_SUFFIXES[storefront]

    return base + suffix

def get_store_info(store):
    STORES = {
    # Germany
    "rosenstrasse": {"number": "R045", "storefront": "de"},
    "oez": {"number": "R521", "storefront": "de"},
    "augsburg": {"number": "R431", "storefront": "de"},

    # France — Paris and surrounding area
    "champs-elysees": {"number": "R675", "storefront": "fr"},
    "opera": {"number": "R277", "storefront": "fr"},
    "marche-saint-germain": {"number": "R566", "storefront": "fr"},
    "la-defense": {"number": "R178", "storefront": "fr"},
    "rosny-2": {"number": "R536", "storefront": "fr"},
    "velizy-2": {"number": "R315", "storefront": "fr"},
    "parly-2": {"number": "R374", "storefront": "fr"},
    "carre-senart": {"number": "R438", "storefront": "fr"},
    "val-d-europe": {"number": "R425", "storefront": "fr"},

    # Switzerland
    "rennweg": {"number": "R159", "storefront": "ch-de"},
    "glattzentrum": {"number": "R309", "storefront": "ch-de"},
    "basel": {"number": "R439", "storefront": "ch-de"},
    "geneva": {"number": "R275", "storefront": "ch-fr"},
    }

    return STORES[store]