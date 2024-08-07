from STM import STM
import Utils
import os

# set file path to retrieve the data
folder_path = os.getcwd() + '/ESM_Code/EDIT_Code/'
file_path = folder_path + '065X_STM.txt'
plant_path = folder_path + "065X_annualProduction.txt"

p = open(plant_path, 'r')
lines = p.readlines()
plant_data = Utils.txtToDF(lines)
plant_data = plant_data[plant_data['"Ecological site ID"'] == 'R065XY029NE']

# change the column name
plant_data.columns = ['MLRA', '"Ecological site ID"', '"Ecological site legacy ID"',
       '"Land use"', '"Ecosystem state"', '"Plant community"', '"Plant type"',
       '"Production low"', '"Production RV"', '"Production high"']

# process the last column
plant_data['"Production high"'] = plant_data['"Production high"'].apply(lambda x: x.replace('\n', ''))

plant_data['"Plant community"'] = plant_data['"Ecosystem state"'] + '.' + plant_data['"Plant community"']

with open(file_path) as f:
    lines = f.readlines()

    # split column into multi
    state_data = Utils.txtToDF(lines)

    # to locate the ES site
    state_data = state_data[state_data['"Ecological site ID"'] == 'R065XY029NE']

    # create the graph object for R055BY056ND
    graph = STM()

    # add states
    node_text = state_data[state_data['"State type"'] == '"ecosystem state"']

    for index, row in node_text.iterrows():
        state_id = row['"Ecosystem state"']
        state_name = row['Name']
        meta = row['Description']
        graph.add_state(state_id= state_id, name= state_name, meta= meta)

    # add plant community for each state
    plant_text = state_data[state_data['"State type"'] == '"plant community"']
    # change the plant community id
    plant_text['"Plant community"'] = plant_text['"Ecosystem state"'] + '.' + plant_text['"Plant community"']

    for index, row in plant_text.iterrows():
        state_id = row['"Ecosystem state"']
        plant_id = row['"Plant community"']
        meta = row['Description']
        plant_name = row['Name']

        rp_low, rp_high, rp = {}, {}, {}
        for y, x in plant_data[plant_data['"Plant community"'] == plant_id].iterrows():
            rp_low[x['"Plant type"']] = x['"Production low"']
            rp_high[x['"Plant type"']] = x['"Production high"'].replace('\n','')
            rp[x['"Plant type"']] = x['"Production RV"']

        graph.add_plant_communities_to_state(state_id= state_id, plant_id= plant_id, plant_name= plant_name, rp_low= rp_low, rp_high= rp_high, rp= rp)

p.close()

# add transition
file_path = folder_path + "065X_STMT.txt"
p = open(file_path, 'r')
lines = p.readlines()
transition_data = Utils.txtToDF(lines)
transition_data = transition_data[transition_data['"Ecological site ID"'] == 'R065XY029NE']

# get the transition data
transition_data['"Transition type"'] = transition_data['"Transition type"'].apply(lambda x: x.replace('"restoration pathway"', 'transition'))
transition_data['"Transition type"'] = transition_data['"Transition type"'].apply(lambda x: x.split(' ')[-1])
transition_data['"Transition type"'] = transition_data['"Transition type"'].apply(lambda x: x.replace('"', ''))
stmt_text = transition_data[transition_data['"Transition type"'] == "transition"]

for idx, item in stmt_text.iterrows():
    frm_node = item['"From ecosystem state"']
    to_node = item['"To ecosystem state"']
    trigger = item['Mechanism']
    graph.add_transition(frm= frm_node, to= to_node, trigger= trigger)

# add pathway
stmt_plant = transition_data[transition_data['"Transition type"'] == 'pathway']
# change the plant community id for pathway
stmt_plant['"From plant community"'] = stmt_plant['"From ecosystem state"'] + '.' + stmt_plant['"From plant community"']
stmt_plant['"To plant community"'] = stmt_plant['"To ecosystem state"'] + '.' + stmt_plant['"To plant community"']

for idx, item in stmt_plant.iterrows():
    graph.add_pathway(state_id= item['"From ecosystem state"'], frm= item['"From plant community"'],
                     to= item['"To plant community"'], trigger= item['Mechanism'])

# with annotation and interactive
Utils.interDraw(graph= graph, node_txt= node_text, plant_data= plant_data, stmt_text= stmt_text, stmt_plant= stmt_plant)
