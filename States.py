from PlantCommunity import PlantCommunity

class States:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.adjacent = {}
        self.plant_community = {}

    def add_neighbor(self, neighbor, trigger):
        self.adjacent[neighbor] = trigger

    def add_plant_community(self, id, name,rp_low, rp_high, growth_curve):
        new_plantcumm = PlantCommunity(id, name)
        new_plantcumm.add_plant_data(rp_low, rp_high, growth_curve)
        self.plant_community[id] = new_plantcumm

    def get_plant_community(self):
        return self.plant_community.keys()

    def get_connections(self):
        return self.adjacent.keys()

    def get_trigger(self, neighbor):
        return self.adjacent[neighbor]