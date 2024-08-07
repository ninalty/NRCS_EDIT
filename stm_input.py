import pandas as pd

# heading == 3
states = pd.DataFrame({'state type': [],
                       'state': [],
                       'community': [],
                       'name': [],
                       'description': [],
                       'plant type': [],
                       'production low': [],
                       'production RV': [],
                       'production high': [],
                       'plant growthC': []})


# heading == 4
transition = pd.DataFrame({'transition type': [],
                           'from state': [],
                           'from community': [],
                           'to state': [],
                           'to community': [],
                           'name': [],
                           'mechanism': []})

file_path = "./UCD_ES_Project/ESM_EDIT/ESM_EDIT_Data/ESM_EDIT_Features/STM_state/065X_STM.txt"

with open(file_path) as f:
    lines = f.readlines()

    col_names = lines[2].split('\t')
    df = pd.DataFrame(lines[3:])
    df.columns = ['txt']

    # split column into multi
    STMT = pd.DataFrame(df['txt'].str.split('\t').values.tolist())
    STMT.columns = col_names

    # to locate the ES site
    row = STMT[STMT[col_names[1]] == 'R065XY011NE']

    transition.loc[len(transition.index)] = [class_seq[idx], '', ' ', '']
