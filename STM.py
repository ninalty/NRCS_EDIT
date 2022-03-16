from States import States

class STM:
    # add a metadata here
    def __init__(self):
        self.vert_dict = {}
        self.num_states = 0
        self.ESID = ''
        self.associated_sites = []

    # add state node to the STM
    def addState(self, state_id, name, meta):
        self.num_states = self.num_states + 1
        new_vertex = States(state_id, name)
        new_vertex.meta = meta
        self.vert_dict[state_id] = new_vertex

    # add plant communities to the state
    def addPlantCummsTostate(self, state_id, plant_id, plant_name,rp_low, rp_high, rp, growth_curve):
        state = self.__getVertex(state_id)
        state.addPlantCommunity(plant_id, plant_name, rp_low, rp_high, rp, growth_curve)

    # build edges between plant communities
    def addPathway(self, state_id, frm, to, trigger):
        state = self.__getVertex(state_id)
        state.plant_community[frm].add_neighbor(state.plant_community[to], trigger)

    def __getVertex(self, id):
        if id in self.vert_dict:
            return self.vert_dict[id]
        else:
            return None

    # add edges between states
    def addTransition(self, frm, to, trigger):
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], trigger)

    # return a list of neighbors of one state
    def getStateList(self):
        return list(self.vert_dict.keys())

    # return a list of neighbors of one plant community
    def getCommList(self, state_id):
        state = self.__getVertex(state_id)
        return list(state.plant_community.keys())
