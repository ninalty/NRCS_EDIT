from typing import Mapping, Dict
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class PlantCommunity:
    id: str
    name: str
    meta: str = ''
    plant_rp_low: Dict[str, float] = field(default_factory=dict)
    plant_rp_high: Dict[str, float] = field(default_factory=dict)
    plant_growth_curve: str = ''
    adjacent: Dict[str, 'PlantCommunity'] = field(default_factory=dict)

    def add_neighbor(self, neighbor: 'PlantCommunity', trigger: str) -> None:
        self.adjacent[trigger] = neighbor

@dataclass
class State:
    id: str
    name: str
    meta: str = ''
    adjacent: Dict[str, 'State'] = field(default_factory=dict)
    plant_community: Dict[str, PlantCommunity] = field(default_factory=dict)

    def add_plant_community(self, plant_id: str, comm_name: str, rp_low: Dict[str, float], rp_high: Dict[str, float], growth_curve: str) -> None:
        new_plant_comm = PlantCommunity(id=plant_id, name=comm_name, plant_rp_low=rp_low, plant_rp_high=rp_high, plant_growth_curve=growth_curve)
        self.plant_community[plant_id] = new_plant_comm

    def add_neighbor(self, neighbor: 'State', trigger: str) -> None:
        self.adjacent[trigger] = neighbor
