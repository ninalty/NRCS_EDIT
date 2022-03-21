from STM import STM
import Utils
import pandas as pd

# set file path to retrieve the data
file_path = '/Users/x-women/Desktop/UCD_ES_Project/ESM_EDIT/ESM_EDIT_Data/ESM_DataStructure/es_inputData/DS_R055BY056ND.xlsx'
input_file = pd.read_excel(file_path, sheet_name='states')
input_file = pd.DataFrame(input_file)

# create the graph object for R055BY056ND
graph = STM()

# add states
node_text = input_file[input_file['state type'] == "state"]

for index, row in node_text.iterrows():
    state_id = row['state']
    state_name = row['name']
    meta = row['Description']
    graph.addState(state_id= state_id, name= state_name, meta= meta)

# add plant community for each state
plant_text = input_file[input_file['state type'] == "community"]

for index, row in plant_text.iterrows():
    state_id = row['state']
    plant_id = row['community']
    meta = row['Description']
    plant_name = row['name']
    meta = row['Description']
    growth_curve = row['plant_growth_curve']

    rp_low, rp_high, rp = {}, {}, {}
    for y, x in plant_text[plant_text['community'] == plant_id].iterrows():
        rp_low[x['plant type']] = x['production low']
        rp_high[x['plant type']] = x['production high']
        rp[x['plant type']] = x['production RV']

    graph.addPlantCummsTostate(state_id, plant_id, plant_name,
                               rp_low= rp_low, rp_high= rp_high, rp = rp, growth_curve= growth_curve)

# add transition
input_file = pd.read_excel(file_path, sheet_name='transition')
input_file = pd.DataFrame(input_file)
stmt_text = input_file[input_file['Transition type'] == "transition"]

for idx, item in stmt_text.iterrows():
    frm_node = item['From state']
    to_node = item['To state']
    trigger = item['Mechanism']
    graph.addTransition(frm= frm_node, to= to_node, trigger= trigger)

# add pathway
stmt_plant = input_file[input_file['Transition type'] == 'pathway']
for idx, item in stmt_plant.iterrows():
    graph.addPathway(state_id= item['From state'], frm= item['From community'],
                     to= item['To community'], trigger= item['Mechanism'])

# graph visualization
# Utils.draw(graph_model=graph, title='ES ID State Transition Model', file_name= 'node2.html')

# with annotation and interactive
Utils.interDraw(graph, 'ttt', node_text, plant_text, stmt_text, stmt_plant)
