from typing import Mapping

# class to build plant community nodes
class PlantCommunity:
    def __init__(self, id, name):
        # identification of plant community
        self.id: str = id
        # name of the plant community
        self.name: str = name
        # description of plant community
        self.meta: str = ''
        # representative low production
        self.plant_rp_low: Mapping[str, float] = {}
        # representative high production
        self.plant_rp_high: Mapping[str, float] = {}
        # plant growth curve. is a str can turn to {month: production of dominant plant}
        self.plant_growth_curve: str = ''
        # {triggers: PlantCommunity node}
        self.adjacent: Mapping[str, object] = {}

    def add_neighbor(self, neighbor, trigger):
        self.adjacent[trigger] = neighbor

# class for states. plantCommunity class will be called to build plant nodes within the state
class States:
    def __init__(self, id, name):
        # identification of state
        self.id: str = id

        # name of the state
        self.name: str = name

        # description of the state
        self.meta: str = ''

        # {trigger: States node}
        self.adjacent: Mapping[str, object] = {}

        # {plant_id: PlantCommunity node}
        self.plant_community: Mapping[str, object] = {}

    # plantCommunity class called to build plant nodes within the state
    def addPlantCommunity(self, plant_id, comm_name, rp_low, rp_high, rp, growth_curve):

        # create a new PlantCommunity node with assigned id and name
        new_plantcumm = PlantCommunity(plant_id, comm_name)

        # get all the input filled to the node features
        new_plantcumm.plant_rp_low = rp_low
        new_plantcumm.plant_rp_high = rp_high
        new_plantcumm.plant_rp = rp
        new_plantcumm.plant_rp_low = growth_curve

        # add this new PlantCommunity node to state's plant community holder
        self.plant_community[plant_id] = new_plantcumm

    def add_neighbor(self, neighbor, trigger):
        self.adjacent[trigger] = neighbor