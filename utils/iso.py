# utils/iso.py

country_aliases = {
    "UK": "GB",
    "USA": "US",
    "UAE": "AE",
    "South Korea": "KR",
    "Iran": "IR",
    "Russia": "RU",
    "China": "CN",
    "France": "FR",
    "Germany": "DE",
    "Brazil": "BR",
    "Pakistan": "PK",
    "Singapore": "SG",
    "Nigeria": "NG",
    "Japan": "JP",
    "Mexico": "MX",
    "Canada": "CA",
    "Taiwan": "TW",
    "Turkey": "TR",
    "Australia": "AU",
    "Saudi Arabia": "SA",
    "South Africa": "ZA",
    "Israel": "IL",
    "Bangladesh": "BD"
}


def get_country_code(name: str) -> str:
    if name in country_aliases:
        return country_aliases[name]
    return None
