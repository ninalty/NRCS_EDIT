import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from netgraph import InteractiveGraph, Graph
from pyvis.network import Network
import mpld3

# graph model visualization
def draw(graph_model, title, file_name):
    net = Network(directed=True, heading=title, width='100%')

    for node in graph_model.vert_dict.values():
        net.add_node(node.id, label=node.id,shape='square', size=30, group = 1)

        for plant_node in node.plant_community.values():
            net.add_node(str(plant_node.id), label=str(plant_node.id), color='#eb4034', size = 10, group = 2)

        # add edges
    for node in graph_model.vert_dict.values():
        if node.adjacent:
            for key, nei in node.adjacent.items():
                net.add_edge(node.id, nei.id)

        # connect node to one of its plant node
        a = node.plant_community.keys()
        a = list(a)[0]
        net.add_edge(node.id, str(a))

        # add pathway between communities
        for plant_node in node.plant_community.values():
            if plant_node.adjacent:
                for key, nei in plant_node.adjacent.items():
                    net.add_edge(str(plant_node.id), str(nei.id))

    net.set_edge_smooth('dynamic')
    net.show(file_name)

# interactive graph
def interDraw(graph, file_name):
    tables = dict()

    net = nx.Graph()
    node_sizes = {}
    node_shapes = {}
    node_colors = {}
    for node in graph.vert_dict.values():
        net.add_node(node.id)
        node_sizes[node.id] = 8
        node_shapes[node.id] = 's'
        node_colors[node.id] = 'red'

        for plant_node in node.plant_community.values():
            net.add_node(str(plant_node.id))
            node_sizes[str(plant_node.id)] = 4
            node_shapes[str(plant_node.id)] = 'o'
            node_colors[str(plant_node.id)] = 'white'

        # add edges
    for node in graph.vert_dict.values():
        if node.adjacent:
            for key, nei in node.adjacent.items():
                net.add_edge(node.id, nei.id)

        # connect node to one of its plant node
        a = node.plant_community.keys()
        a = list(a)[0]
        net.add_edge(node.id, str(a))

        # add pathway between communities
        for plant_node in node.plant_community.values():
            if plant_node.adjacent:
                for key, nei in plant_node.adjacent.items():
                    net.add_edge(str(plant_node.id), str(nei.id))

    # add notation
    for node in net.nodes:
        data = np.round(np.random.rand(2, 1), decimals=2)
        table = pd.DataFrame(data, index=['Name', '  '], columns=[''])
        tables[node] = table

    for edge in net.edges:
        data = np.round(np.random.rand(2, 3), decimals=2)
        table = pd.DataFrame(data, index=[' ', '  '], columns=['from', 'to', 'Triggers'])
        tables[edge] = table

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.subplots_adjust(right=0.6)  # make space for table on the right
    bbox = [1.2, 0.1, 0.5, 0.8]  # position of the table in axes coordinates
    instance = InteractiveGraph(net, node_size=node_sizes, node_shape=node_shapes, node_color=node_colors,
                                node_labels=True, tables=tables,
                                table_kwargs=dict(edges='horizontal', fontsize=10, bbox=bbox), ax=ax)
    # mpld3.save_html(fig,'year.html', template_type='simple')
    plt.show()


# return a list of neighbors' id of the designated node
def getNeighborList(node):
    return node.adjacent.items()

# retrieve the trigger between two nodes
def getTrigger(node, neighbor):
    for key, item in node.adjacent.items():
        if item == neighbor:
            return key