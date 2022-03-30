import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from netgraph import InteractiveGraph
from pyvis.network import Network

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

def __wrap(string, max_width):
    s=''
    for i in range(0, len(string), max_width):
        s += string[i:i+max_width]
        s += '\n'
    return s

# turn txt to dataframe
def txtToDF(input):
    col_names = input[2].split('\t')
    df = pd.DataFrame(input[3:])
    df.columns = ['txt']

    # split column into multi
    state_data = pd.DataFrame(df['txt'].str.split('\t').values.tolist())
    state_data.columns = col_names

    return state_data

# interactive graph
def interDraw(graph, node_txt, plant_data, stmt_text, stmt_plant):
    tables = dict()

    net = nx.Graph()
    node_sizes = {}
    node_shapes = {}
    node_colors = {}
    edge_colors = {}
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
                edge_colors[node.id, nei.id] = 'red'

        # connect node to one of its plant node
        a = node.plant_community.keys()
        a = list(a)[0]
        net.add_edge(node.id, str(a), key= 'transition')
        edge_colors[(node.id, str(a))] = 'silver'

        # add pathway between communities
        for plant_node in node.plant_community.values():
            if plant_node.adjacent:
                for key, nei in plant_node.adjacent.items():
                    net.add_edge(str(plant_node.id), str(nei.id), key= 'pathyway')
                    edge_colors[(str(plant_node.id), str(nei.id))] = 'black'

    # add notation
    # state nodes
    for node in net.nodes:
        if len(node) == 1:

            row = node_txt[node_txt['"Ecosystem state"'] == node]
            data = [_ for _ in row['Description']]
            col_name = [_ for _ in row['Name']][0]
            data = {col_name: data[0].split('.')[0]}
            table = pd.DataFrame(data, index=[''])
            table[col_name] = table[col_name].str.wrap(50)
            tables[node] = table

        # plant nodes
        else:
            row = plant_data[plant_data['"Plant community"'] == float(node)]
            if row.shape[0] != 1:
            # plant_name = [elm for elm in row['plant type']]
                plant_comp = [plant_data['"Production low"'], plant_data['"Production RV"'], plant_data['"Production high"']]

                data = [[elm for elm in plant_comp[0]],
                        [elm for elm in plant_comp[1]],
                         [elm for elm in plant_comp[2]]]

            # no record on plant composition
            else:
                data = [[0] * 3 for i in range(3)]

            table = pd.DataFrame(data, index=['shrub/vine', 'grass/grasslike', 'forb'], columns=['p_low', 'p_RV', 'p_high'])
            tables[node] = table

    for edge in net.edges:
        if len(edge[0]) == 1 and len(edge[1]) == 1:
            row = stmt_text[stmt_text['"From ecosystem state"'] == edge[0]]
            row = row[row['"To ecosystem state"'] == edge[1]]
            mech = [_ for _ in row['Mechanism']][0].split('.')[0]
            mech = __wrap(mech, 60)
            data = [[_ for _ in row['"From ecosystem state"']], [_ for _ in row['"To ecosystem state"']]]
            data = [str(x[0]) for x in data]
            table = pd.DataFrame(data, index=['from', 'to'], columns=[mech])
            tables[edge] = table

        elif len(edge[0]) != 1 and len(edge[1]) != 1:
            row = stmt_plant[stmt_plant['"From plant community"'] == edge[0]]
            row = row[row['"To plant community"'] == edge[1]]
            mech = [_ for _ in row['Mechanism']][0].split('.')[0]
            mech = __wrap(mech, 60)
            data = [[_ for _ in row['"From plant community"']], [_ for _ in row['"To plant community"']]]
            data = [str(x[0]) for x in data]
            table = pd.DataFrame(data, index=['from', 'to'], columns=[mech])
            tables[edge] = table

        else:
            table = ['plant community of the state']
            tables[edge] = table

    fig, ax = plt.subplots(figsize=(14, 8))
    fig.subplots_adjust(right=0.6)  # make space for table on the right
    bbox = [1.2, 0.1, 0.5, 0.8]  # position of the table in axes coordinates
    instance = InteractiveGraph(net, node_size=node_sizes, node_shape=node_shapes, node_color=node_colors,
                                node_labels=True, tables=tables, node_layout = 'dot', edge_layout= 'curved',
                                edge_color = edge_colors, edge_alpha = 1,
                                table_kwargs=dict(edges='horizontal', fontsize=10, bbox=bbox), ax=ax)

    plt.show()

# return a list of neighbors' id of the designated node
def getNeighborList(node):
    return node.adjacent.items()

# retrieve the trigger between two nodes
def getTrigger(node, neighbor):
    for key, item in node.adjacent.items():
        if item == neighbor:
            return key