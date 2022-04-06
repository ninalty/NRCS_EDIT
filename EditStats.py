import glob
import Utils
import pandas

# set file path to retrieve the data
folder_path = '/Users/x-women/Desktop/UCD_ES_Project/ESM_EDIT/ESM_EDIT_Data/ESM_EDIT_Features/'
state_path = folder_path + 'STM_state/'
production_path = folder_path + 'annual_production/'
transition_path = folder_path + 'STM_Transition/'

# check whether STM exist
transition_files = glob.glob(transition_path + '*.txt')

STM_stats = pandas.DataFrame({'MLRA': [],
                             'ES_ID': [],
                             'STM': [],
                              'row_no': []})

for file in transition_files:

    p = open(file, 'r')
    lines = p.readlines()
    MLRA_id = file.split('/')[-1].split('_')[0]

    try:
        if len(lines) <= 3:
            data = {'MLRA': MLRA_id, 'ES_ID': 'NA', 'STM': False, 'row_no': 0}
            STM_stats = STM_stats.append(data, ignore_index=True)

        else:
            mlra_data = Utils.txtToDF(lines)
            es_id = mlra_data[mlra_data['MLRA'] == MLRA_id]['"Ecological site ID"'].unique().tolist()

            # iterate through es id for each mlra
            for id in es_id:
                es_data = mlra_data[mlra_data['"Ecological site ID"'] == id]

                if es_data.shape[0] > 0:
                    data = {'MLRA': MLRA_id, 'ES_ID': id, 'STM': True, 'row_no': es_data.shape[0]}
                    STM_stats = STM_stats.append(data, ignore_index=True)
                else:
                    data = {'MLRA': MLRA_id, 'ES_ID': id, 'STM': False, 'row_no': es_data.shape[0]}
                    STM_stats = STM_stats.append(data, ignore_index=True)

                es_data = []
    except:
        print(MLRA_id)

# STM_stats.to_csv('STM_stats.csv', index=False)
