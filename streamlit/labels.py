# Here we have all the labels for our category columns

import json
from pathlib import Path

POSTAL_DATA_PATH = Path(__file__).parent / "data" / "zipcode-belgium.json"

with open(POSTAL_DATA_PATH, encoding="utf-8") as f:
    _postal_data = json.load(f)

CITY_OPTIONS = {
    f"{entry['zip']} – {entry['city']}": entry
    for entry in _postal_data
}

PROVINCE_OPTIONS = [
    "brussels", "vlaams_brabant", "antwerp", "east_flanders",
    "west_flanders", "brabant_wallon", "limburg", "hainaut",
    "namur", "liege", "luxembourg",
]
TYPE_PROPERTY_OPTIONS = ["house", "apartment"]
SUBTYPE_PROPERTY_OPTIONS = [
    "residence", "studio", "apartment", "duplex", "mixed_building",
    "penthouse", "villa", "ground_floor", "loft", "triplex",
    "master_house", "bungalow", "chalet", "cottage", "mansion",
]

SUN_EXPOSURE_LABELS = {
    "not_specified": "Not Specified", "south": "South", "south_east": "South East",
    "east": "East", "north_east": "North East", "north": "North",
    "north_west": "North West", "west": "West", "south_west": "South West",
}
HEATING_TYPE_LABELS = {
    "not_specified": "Not Specified", "gas": "Gas", "electricity": "Electricity",
    "fuel_oil": "Fuel Oil", "hot_air": "Hot Air", "coal": "Coal",
    "wood": "Wood", "solar_energy": "Solar Energy",
}
STATE_OF_PROPERTY_LABELS = {
    "not_specified": "Not Specified", "new": "New", "excellent": "Excellent",
    "normal": "Normal", "to_be_renovated": "To Be Renovated",
    "to_renovate": "To Renovate", "fully_renovated": "Fully Renovated",
    "to_restore": "To Restore", "to_demolish": "To Demolish",
    "under_construction": "Under Construction",
}
EPC_SCORE_LABELS = {
    "not_specified": "Not Specified", "a+": "A+", "a": "A", "b": "B",
    "c": "C", "d": "D", "e": "E", "f": "F", "g": "G",
}
FLOODING_AREA_LABELS = {
    "(information_not_available)": "Not Available", "no_flooding_area": "No Flooding Risk",
    "low_risk": "Low Risk", "possible_flooding_area": "Possible Flooding Area",
    "actual_flooding_area": "Actual Flooding Area",
}