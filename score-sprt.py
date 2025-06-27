# import framework (PANDAS) for manipulating data: https://pandas.pydata.org/ (reason for pip and venv)
import pandas as pd
# library for reading all files in a directory: https://docs.python.org/3/library/glob.html
import glob
# library for mathematical functions: https://docs.python.org/3/library/math.html
import math

import re
# read all matching file names in ./SPRT_csv folder
# this variable is a list of strings, all which are present relative to current working directory and in form 'NBack_csv/C2xxx_DualNBack_Task_*.csv'
files = glob.glob('Participant sub-folders/sub_C????//C????_SRT_*.csv')

# process files in order by PID
files = sorted(files)

# empty dataframe to store relavent results
results = pd.DataFrame(columns=['PID', 'EASY_AVG_CORR_RT', 'EASY_AVG_INCORR_RT', 'EASY_ACC', 'HARD_AVG_CORR_RT', 'HARD_AVG_INCORR_RT', 'HARD_ACC'])

print(f'Reading {len(files)} CSV files from ./SPRT_csv folder...')

# iterate through each file found in subdirectory
for f in files:

    # show full path and filename
    print(f)

    # extract filename from path and PID from filename
    filename = re.split(r"[\\/]", f)[2]
    pid = ''.join(list(filename)[1:5])
    
    # read data into dataframe from local file
    df = pd.read_csv(f)

    # filter out relavent columns and remove rows where all relavent columns are N/A
    relavent_columns = ["target", "stim_2", "RESP.time", "RESP.clicked_name"]
    df = df[relavent_columns].dropna(how='all', subset=['RESP.time'])

    # remove first two rows of dataframe (these are practice trials)
    df = df.iloc[2:]

    # add 'distance' column to dataframe (distance between target and decoy), and calculate value for each row
    for row in df.iterrows():

        # extract coordinates from target and decoy (convert to float)
        corr = row[1].loc['target'].split(',')
        corr_coord = [float(c) for c in corr]
        incorr = row[1].loc['stim_2'].split(',')
        incorr_coord = [float(c) for c in incorr]

        distance = math.dist(corr_coord, incorr_coord)
        # add distance to dataframe at this row's index, and the 'distance' column
        df.loc[row[0] , 'distance'] = distance

    # change 'RESP.clicked_name' to 0 if incorrect, 1 if correct
    def zero_if_incorrect(x):
        if x != '[\'target_image\']': return 0
        else: return 1

    # remove brackets from 'RESP.time' column, and convert string to float
    # Also, if there are multiple values separated by comma, use only the last value (this is caused by inaccurate clicks by the participant)
    def remove_brackets(x):
        x_without_brackets = x.replace('[', '').replace(']', '')
        if (',' in x_without_brackets):
            y = x_without_brackets.split(',')
            x_without_brackets = y[len(y) - 1]
        return float(x_without_brackets)

    accuracy_col = df['RESP.clicked_name'].apply(zero_if_incorrect)
    df['RESP.clicked_name'] = accuracy_col

    normalize_rt_col = df['RESP.time'].apply(remove_brackets)
    df['RESP.time'] = normalize_rt_col

    # results relavant to easy trials
    easy_df = df[df['distance'] > .25]
    easy_right_df = easy_df[easy_df['RESP.clicked_name'] == 1]
    easy_wrong_df = easy_df[easy_df['RESP.clicked_name'] == 0]
    
    # average correct, incorrect, and total accuracy (for easy)
    easy_avg_correc_rt = easy_right_df['RESP.time'].mean()
    easy_avg_incorr_rt = easy_wrong_df['RESP.time'].mean()
    easy_acc = easy_df['RESP.clicked_name'].mean()
    
    # results relavant to hard trials
    hard_df = df[df['distance'] <= .25]
    hard_right_df = hard_df[hard_df['RESP.clicked_name'] == 1]
    hard_wrong_df = hard_df[hard_df['RESP.clicked_name'] == 0]

    # average correct, incorrect, and total accuracy (for hard)
    hard_avg_correc_rt = hard_right_df['RESP.time'].mean()
    hard_avg_incorr_rt = hard_wrong_df['RESP.time'].mean()
    hard_acc = hard_df['RESP.clicked_name'].mean()

    # add PID and results to return dataframe
    results.loc[len(results.index)] = [pid, easy_avg_correc_rt, easy_avg_incorr_rt, easy_acc, hard_avg_correc_rt, hard_avg_incorr_rt, hard_acc ]



# sort by PID and export CSV
results = results.sort_values(by='PID')
results.to_csv('charm-scoring/sprt_scores.csv', sep=',', index=False)
