import pandas as pd
from dataclasses import dataclass
from typing import Mapping, Sequence

@dataclass
class States:
    general_info: str
    states_id: list[str]
    states_name: str
    triggers: list[str]
    # variable
    # plant_community: Mapping[PlantCommunity, float] # indicate the type
    plant_community: PlantCommunity

@dataclass
class PlantCommunity:
    plant_commID: str
    plant_commName: str
    plant_community_type: Sequence[str]
    # think about mapping type to low and high
    plant_production_low: Mapping[str, float]
    plant_production_high: Mapping[str, float]
    plant_commty_growth_curve: list[str]

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
    #
    # def __str__(self):
    #     return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    # def __iter__(self):
    #     return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, trigger):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], trigger)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], trigger)

    def get_vertices(self):
        return self.vert_dict.keys()

def build_STM(file_path):
    file = pd.read_excel(file_path, sheet_name="STM", index_col=0)
    States.states_id = set(file.iloc('Ecosystem state'))
    PlantCommunity.plant_CommID = set(file.iloc(''))

    # add all states as vertex
    STM = Graph()
    for elm in STM.states_id:
        STM.add_vertex(elm)

    # build transition
    STM.add_edge('state1', 'state2', 'trigger1')
    STM.add_edge('state2', 'state3', 'trigger2')
    STM.add_edge('state3', 'state4', 'trigger3')

    return States

# also need to deal with plant community within each


