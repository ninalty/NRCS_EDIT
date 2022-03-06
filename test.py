from STM import STM

# create the graph object for R055BY056ND
graph = STM()

# add states
graph.add_state(1,'Reference State')
graph.add_state(2, 'Native/Invaded State')
graph.add_state(3, "Invaded Grass State")

# build transition between states
graph.add_edge(1, 2, 'Introduction of non-native species')
graph.add_edge(2, 3, 'long-term rest from grazing and fire')
graph.add_edge(3, 2, 'range seeding with native species with management to control invasive species')

# plant communities
# state 1 plant community 1
graph.add_plant_cumms(1, 1, 'Green Needlegrass/Western Wheatgrass',
                      # rp_low
                      {'shrub/vine': 25, 'grass/grasslike': 1650, 'forb': 125},
                      # rp_high
                      {'shrub/vine': 135, 'grass/grasslike': 2990, 'forb': 275},
                      # growth_curve
                      {1:0,2:0,3:3,4:7,5:23,6:42,7:15,8:5,9:4,10:1,11:0,12:0})

# state 1 plant community 2
graph.add_plant_cumms(1, 2, 'Western Wheatgrass/Blue Grama/Sedge/Green Needlegrass',
                      # rp_low
                      None,
                      # rp_high
                      None,
                      # growth_curve
                      {1:0,2:0,3:3,4:7,5:23,6:42,7:15,8:5,9:4,10:1,11:0,12:0})

# build pathway between plant community 1.1 and 1.2
graph.add_pathway(1, 1, 2, 'spring fire followed by intensive grazing')
graph.add_pathway(1, 2, 1, 'return to normal fire and grazing frequencies')

# to know the number of states
graph.get_state_list()
# or
graph.num_states

# to know the number of plant communities of a state
graph.get_comm_list(1)