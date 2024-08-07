from typing import List, Optional, Dict
from States import State

class STM:
    """
    A class to represent a State Transition Model (STM).
    """

    def __init__(self):
        self.vert_dict: Dict[str, State] = {}
        self.num_states: int = 0
        self.ESID: str = ''
        self.associated_sites: List[str] = []

    def add_state(self, state_id: str, name: str, meta: str) -> None:
        """
        Add a state node to the STM.
        
        :param state_id: Unique identifier for the state.
        :param name: Name of the state.
        :param meta: Metadata for the state.
        """
        self.num_states += 1
        new_vertex = State(state_id, name)
        new_vertex.meta = meta
        self.vert_dict[state_id] = new_vertex

    def add_plant_communities_to_state(self, state_id: str, plant_id: str, plant_name: str, rp_low: Optional[Dict[str, float]] = None, rp_high: Optional[Dict[str, float]] = None, rp: Optional[Dict[str, float]] = None, growth_curve: Optional[str] = None) -> None:
        """
        Add plant communities to a state.
        
        :param state_id: ID of the state.
        :param plant_id: ID of the plant community.
        :param plant_name: Name of the plant community.
        :param rp_low: Representative low production.
        :param rp_high: Representative high production.
        :param rp: Plant production.
        :param growth_curve: Growth curve information.
        """
        state = self._get_vertex(state_id)
        if state:
            state.add_plant_community(plant_id, plant_name, rp_low, rp_high, growth_curve)

    def add_pathway(self, state_id: str, frm: str, to: str, trigger: str) -> None:
        """
        Build edges between plant communities.
        
        :param state_id: ID of the state.
        :param frm: ID of the source plant community.
        :param to: ID of the destination plant community.
        :param trigger: Trigger for the pathway.
        """
        state = self._get_vertex(state_id)
        if state and frm in state.plant_community and to in state.plant_community:
            state.plant_community[frm].add_neighbor(state.plant_community[to], trigger)

    def _get_vertex(self, id: str) -> Optional[State]:
        """
        Get a state vertex by its ID.
        
        :param id: ID of the state.
        :return: State object if found, None otherwise.
        """
        return self.vert_dict.get(id)

    def add_transition(self, frm: str, to: str, trigger: str) -> None:
        """
        Add edges between states.
        
        :param frm: ID of the source state.
        :param to: ID of the destination state.
        :param trigger: Trigger for the transition.
        """
        if frm in self.vert_dict and to in self.vert_dict:
            self.vert_dict[frm].add_neighbor(self.vert_dict[to], trigger)

    def get_state_list(self) -> List[str]:
        """
        Get a list of all state IDs.
        
        :return: List of state IDs.
        """
        return list(self.vert_dict.keys())

    def get_community_list(self, state_id: str) -> List[str]:
        """
        Get a list of plant community IDs within a state.
        
        :param state_id: ID of the state.
        :return: List of plant community IDs if state is found, empty list otherwise.
        """
        state = self._get_vertex(state_id)
        if state:
            return list(state.plant_community.keys())
        return []
