from States import States

class STM:
    def __init__(self):
        self.vert_dict = {}
        self.num_states = 0

    def add_state(self, id, name):
        self.num_states = self.num_states + 1
        new_vertex = States(id, name)
        self.vert_dict[id] = new_vertex

    def add_plant_cumms(self, state_id, plant_id, plant_name,rp_low, rp_high, growth_curve):
        state = self.get_vertex(state_id)
        state.add_plant_community(plant_id, plant_name, rp_high, rp_high, growth_curve)

    def add_pathway(self, state_id, frm, to, trigger):
        state = self.get_vertex(state_id)
        state.plant_community[frm].add_neighbor(state.plant_community[to], trigger)

    def get_vertex(self, id):
        if id in self.vert_dict:
            return self.vert_dict[id]
        else:
            return None

    def add_edge(self, frm, to, trigger):
        self.vert_dict[frm].add_neighbor(self.vert_dict[to], trigger)

    def get_state_list(self):
        return self.vert_dict.keys()

    def get_comm_list(self, state_id):
        state = self.get_vertex(state_id)
        return state.plant_community.keys()
