from typing import Mapping

class PlantCommunity:
    def __init__(self, id, name):
        self.id: str = id
        self.name: str = name
        self.plant_rp_low: Mapping[str, float] = {}
        self.plant_rp_high: Mapping[str, float] = {}
        self.plant_growth_curve: Mapping[int, float] = {}
        self.adjacent = {}