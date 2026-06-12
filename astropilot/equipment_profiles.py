import math

import json
import math
from pathlib import Path

json_path = Path(__file__).parent / "equipment_profiles.json"

with open(json_path, "r", encoding="utf-8") as f:
    EQUIPMENT_PROFILES = json.load(f)

CURRENT_EQUIPMENT = "redcat51_asi2600"
EQUIPMENT_PROFILES = {
    "redcat51_2600": {
        "name": "RedCat 51 + ASI2600MC",
        "focal_length_mm": 250,
        "sensor_width_mm": 23.5,
        "sensor_height_mm": 15.7,
    },
    "evostar72_533": {
        "name": "Evostar 72ED + ASI533MC",
        "focal_length_mm": 420,
        "sensor_width_mm": 11.3,
        "sensor_height_mm": 11.3,
    },
    "c8_hyperstar_2600": {
        "name": "C8 HyperStar + ASI2600MC",
        "focal_length_mm": 390,
        "sensor_width_mm": 23.5,
        "sensor_height_mm": 15.7,
    },
    "rc8_294": {
        "name": "RC8 + ASI294MC",
        "focal_length_mm": 1625,
        "sensor_width_mm": 19.1,
        "sensor_height_mm": 13.0,
    },

    "samyang135_2600": {
        "name": "Samyang 135 + ASI2600",
        "focal_length_mm": 135,
        "sensor_width_mm": 23.5,
        "sensor_height_mm": 15.7,
    },
}

CURRENT_EQUIPMENT = "samyang135_2600"


def field_of_view_deg(focal_length_mm, sensor_mm):
    return 2 * math.degrees(
        math.atan(sensor_mm / (2 * focal_length_mm))
    )


def get_current_equipment():
    return EQUIPMENT_PROFILES[CURRENT_EQUIPMENT]


def get_fov(equipment=None):
    if equipment is None:
        equipment = get_current_equipment()

    return {
        "width_deg": field_of_view_deg(
            equipment["focal_length_mm"],
            equipment["sensor_width_mm"]
        ),
        "height_deg": field_of_view_deg(
            equipment["focal_length_mm"],
            equipment["sensor_height_mm"]
        ),
        }

def equipment_match_score(object_size_arcmin, object_type="unknown", equipment=None):
    """
    Score d'adéquation entre un objet et le champ du matériel.
    Retourne un score entre 0 et 100.
    """

    if equipment is None:
        equipment = get_current_equipment()

    fov = get_fov(equipment)
    width = fov["width_deg"]
    height = fov["height_deg"]
    frame_diag = math.sqrt(width ** 2 + height ** 2)

    object_size_deg = object_size_arcmin / 60
    ratio = object_size_deg / frame_diag

    if object_type == "planetary_nebula":
        ideal_min = 0.02
        ideal_max = 0.20
    elif object_type == "galaxy":
        ideal_min = 0.08
        ideal_max = 0.25
    elif object_type == "cluster":
        ideal_min = 0.10
        ideal_max = 0.60
    else:
        ideal_min = 0.15
        ideal_max = 0.90

    if ideal_min <= ratio <= ideal_max:
        return 100

    if ratio < ideal_min:
        score = 100 * (ratio / ideal_min)
    else:
        score = 100 * (ideal_max / ratio)

    return max(0, min(100, round(score)))

def set_current_equipment(profile_name):
    global CURRENT_EQUIPMENT

    if profile_name not in EQUIPMENT_PROFILES:
        raise ValueError(f"Profil inconnu : {profile_name}")

    CURRENT_EQUIPMENT = profile_name

def list_equipment():
    return list(EQUIPMENT_PROFILES.keys())
    
