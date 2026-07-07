from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class TypeProperty(str, Enum):
    house = "house"
    apartment = "apartment"

class SubtypeProperty(str, Enum):
    residence = "residence"
    studio = "studio"
    apartment = "apartment"
    duplex = "duplex"
    mixed_building = "mixed_building"
    penthouse = "penthouse"
    villa = "villa"
    ground_floor = "ground_floor"
    loft = "loft"
    triplex = "triplex"
    master_house = "master_house"
    bungalow = "bungalow"
    chalet = "chalet"
    cottage = "cottage"
    mansion = "mansion"

class Province(str, Enum):
    brussels = "brussels"
    vlaams_brabant = "vlaams_brabant"
    antwerp = "antwerp"
    east_flanders = "east_flanders"
    west_flanders = "west_flanders"
    brabant_wallon = "brabant_wallon"
    limburg = "limburg"
    hainaut = "hainaut"
    namur = "namur"
    liege = "liege"
    luxembourg = "luxembourg"

class StateOfProperty(str, Enum):
    to_be_renovated = "to_be_renovated"
    to_renovate = "to_renovate"
    excellent = "excellent"
    normal = "normal"
    not_specified = "not_specified"
    new = "new"
    fully_renovated = "fully_renovated"
    to_demolish = "to_demolish"
    under_construction = "under_construction"
    to_restore = "to_restore"

class HeatingType(str, Enum):
    fuel_oil = "fuel_oil"
    electricity = "electricity"
    not_specified = "not_specified"
    gas = "gas"
    hot_air = "hot_air"
    coal = "coal"
    wood = "wood"
    solar_energy = "solar_energy"

class SunExposure(str, Enum):
    south_east = "south_east"
    not_specified = "not_specified"
    south = "south"
    east = "east"
    south_west = "south_west"
    west = "west"
    north_east = "north_east"
    north = "north"
    north_west = "north_west"

class EpcScore(str, Enum):
    g = "g"
    f = "f"
    e = "e"
    not_specified = "not_specified"
    c = "c"
    d = "d"
    b = "b"
    a = "a"
    a_plus = "a+"

class FloodingAreaType(str, Enum):
    information_not_available = "(information_not_available)"
    no_flooding_area = "no_flooding_area"
    possible_flooding_area = "possible_flooding_area"
    actual_flooding_area = "actual_flooding_area"
    low_risk = "low_risk"

class PropertyInput(BaseModel):
    province: Province
    type_property: TypeProperty
    subtype_property: SubtypeProperty
    state_of_property: StateOfProperty
    heating_type: HeatingType
    sun_exposure: SunExposure
    epc_score: EpcScore
    flooding_area_type: FloodingAreaType

    livable_surface: float
    latitude: float
    longitude: float
    facades: int
    bedrooms: float
    construction_year: float
    bathrooms: int
    toilets: int

    terrace: int = 0
    garden: int = 0
    garage: int = 0
    swimming_pool: int = 0