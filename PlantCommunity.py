from typing import Mapping

class PlantCommunity:
    def __init__(self, id, name):
        self.id: str = id
        self.name: str = name
        self.plant_rp_low: Mapping[str, float] = {}
        self.plant_rp_high: Mapping[str, float] = {}
        self.plant_growth_curve: Mapping[int, float] = {}
        self.adjacent = {}

    def add_neighbor(self, neighbor, trigger):
        self.adjacent[neighbor] = trigger

    def add_plant_data(self, rp_low, rp_high, growth_curve):
        self.plant_rp_low = rp_low
        self.plant_rp_high = rp_high
        self.plant_growth_curve = growth_curve

    def get_connections(self):
        return self.adjacent.keys()

    def get_trigger(self, neighbor):
        return self.adjacent[neighbor]