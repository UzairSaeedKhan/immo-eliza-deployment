import json
from pathlib import Path
import logging

POSTAL_DATA_PATH = Path(__file__).parent.parent / "data" / "zipcode-belgium.json"

BRUSSELS_DEFAULT = {"latitude": 50.8503, "longitude": 4.3517}

with open(POSTAL_DATA_PATH, encoding="utf-8") as f:
    _raw_postal_data = json.load(f)

POSTAL_LOOKUP = {
    int(entry["zip"]): {"latitude": float(entry["lat"]), "longitude": float(entry["lng"])}
    for entry in _raw_postal_data
}

def resolve_coordinates(postal_code: int) -> dict:
    """Return lat/long for a Belgian postal code, defaulting to Brussels."""
    return POSTAL_LOOKUP.get(postal_code, BRUSSELS_DEFAULT)

def get_lat_lng(data: dict) -> dict:
    """Takes user input and adds longitude & latitude to the dictionary using resolve_coordinates()"""
    postal_code = data.pop("postal_code", None)
    coords = resolve_coordinates(postal_code)
    data["latitude"] = coords["latitude"]
    data["longitude"] = coords["longitude"]
    return data

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger