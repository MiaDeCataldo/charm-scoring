# import framework (PANDAS) for manipulating data: https://pandas.pydata.org/
import pandas as pd
import glob
import math

# read all matching file names in ./SPRT_csv folder
# this variable is a list of strings, all which are present and in form 'NBack_csv/C2xxx_DualNBack_Task_*.csv'
files = glob.glob('SPRT_csv/C2???_SRT_*.csv')
#files = glob.glob('SPRT_csv/C2120_SRT_*.csv')

files = sorted(files)

results = pd.DataFrame(columns=['PID', 'EASY_AVG_CORR_RT', 'EASY_AVG_INCORR_RT', 'EASY_ACC', 'HARD_AVG_CORR_RT', 'HARD_AVG_INCORR_RT', 'HARD_ACC'])

# iterate through each file found in subdirectory
for f in files:

    print(f)

    filename = f.split('/')[1]
    # 1. create list of characters from filename
    # 2. access list from the 1st index to the 4th index to find participant ID (skips C for filenames like C2xxx)
    # 3. resulting list is only integers that make up PID. Glue them together with empty string ('') to make one integer
    pid = ''.join(list(filename)[1:5])
    #if pid in ['2012', '2029', '2031', '2054', '2060', '2078', '2122', '2136', '2147']:
    #    continue
    
    # read data into dataframe from local file
    df = pd.read_csv(f)
    relavent_columns = ["target", "stim_2", "RESP.time", "RESP.clicked_name"]

    df = df[relavent_columns].dropna(how='all', subset=['RESP.time'])
    df = df.iloc[2:]

    for row in df.iterrows():

        corr = row[1].loc['target'].split(',')
        corr_coord = [float(c) for c in corr]
        incorr = row[1].loc['stim_2'].split(',')
        incorr_coord = [float(c) for c in incorr]
        #print(corr_coord, incorr_coord)

        distance = math.dist(corr_coord, incorr_coord)
        #print(distance)
        #print('')
        df.loc[row[0] , 'distance'] = distance

    def zero_if_incorrect(x):
        if x != '[\'target_image\']': return 0
        else: return 1

    def remove_brackets(x):
        string_without_brackets = x.replace('[', '')
        string_without_brackets = string_without_brackets.replace(']', '')
        if (',' in string_without_brackets):
            y = string_without_brackets.split(',')
            string_without_brackets = y[len(y) - 1]
        return float(string_without_brackets)

    new_col = df['RESP.clicked_name'].apply(zero_if_incorrect)
    df['RESP.clicked_name'] = new_col

    new_col = df['RESP.time'].apply(remove_brackets)
    df['RESP.time'] = new_col

    easy_df = df[df['distance'] > .25]

    easy_df_corr = easy_df[easy_df['RESP.clicked_name'] == 1]
    easy_avg_corr_rt = easy_df_corr['RESP.time'].mean()

    easy_df_incorr = easy_df[easy_df['RESP.clicked_name'] == 0]
    easy_avg_incorr_rt = easy_df_incorr['RESP.time'].mean()

    easy_acc = easy_df['RESP.clicked_name'].mean()

    #print(easy_avg_corr_rt)
    #print(easy_avg_incorr_rt)
    #print(easy_acc)
    #print()
    
    hard_df = df[df['distance'] <= .25]

    hard_df_corr = hard_df[hard_df['RESP.clicked_name'] == 1]
    hard_avg_corr_rt = hard_df_corr['RESP.time'].mean()

    hard_df_incorr = hard_df[hard_df['RESP.clicked_name'] == 0]
    hard_avg_incorr_rt = hard_df_incorr['RESP.time'].mean()

    hard_acc = hard_df['RESP.clicked_name'].mean()

    #print(hard_avg_corr_rt)
    #print(hard_avg_incorr_rt)
    #print(hard_acc)
    #print('')

    #print(hard_df)
    results.loc[len(results.index)] = [pid, easy_avg_corr_rt, easy_avg_incorr_rt, easy_acc, hard_avg_corr_rt, hard_avg_incorr_rt, hard_acc ]


results = results.sort_values(by='PID')
results.to_csv('sprt_scores.csv', sep=',', index=False)