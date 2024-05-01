# import framework (PANDAS) for manipulating data: https://pandas.pydata.org/
import pandas as pd
import glob


# read all matching file names in ./NBack_csv folder
# this variable is a list of strings, all which are present and in form 'NBack_csv/C2xxx_DualNBack_Task_*.csv'
files = glob.glob('NBack_csv/C2???_DualNBack_Task_*.csv')

# create dataframe to store the output data
results = pd.DataFrame(columns=['PID', '1B_AVG_CORR_RT', '1B_AVG_INCORR_RT', '1B_ACC', '2B_AVG_CORR_RT', '2B_AVG_INCORR_RT', '2B_ACC'])

# iterate through each file found in subdirectory
for f in files:
    
    print(f)
    # read data into dataframe from local file
    df = pd.read_csv(f)

    # names currently include directory; split string at '/' and take second half
    filename = f.split('/')[1]
    # 1. create list of characters from filename
    # 2. access list from the 1st index to the 4th index to find participant ID (skips C for filenames like C2xxx)
    # 3. resulting list is only integers that make up PID. Glue them together with empty string ('') to make one integer
    pid = ''.join(list(filename)[1:5])

    # define list of column names that we want to access
    columns = ['oneback_avg_corr', 'oneback_avg_incorr', 'oneback_corr', 'twoback_avg_corr', 'twoback_avg_incorr', 'twoback_corr']
    # 1. access the raw dataframe at the columns specified above
    # 2. from this view, drop every row that contains ALL null values (only 1 row should contain floats (decimals); all others blank)
    # 3. save new view of dataframe to 'relavant' variable
    relavant = df[columns].dropna(how='all')
    
    # iterate over rows in dataframe (this should only be one row)
    for row in relavant.iterrows():

        # access values in row (row[0] is index)
        row = row[1]
        # access columns in row
        oneback_avg_corr_rt = row.iloc[0]
        oneback_avg_incorr_rt = row.iloc[1]
        oneback_acc = row.iloc[2]

        twoback_avg_corr_rt = row.iloc[3]
        twoback_avg_incorr_rt = row.iloc[4]
        twoback_acc = row.iloc[5]
        
        # save pid and relavent metric to output dataframe
        results.loc[len(results.index)] = [
            pid, 
            oneback_avg_corr_rt, 
            oneback_avg_incorr_rt, 
            oneback_acc, 
            twoback_avg_corr_rt, 
            twoback_avg_incorr_rt, 
            twoback_acc
        ]

    
results = results.sort_values(by='PID')
# export output dataframe to local CSV file
results.to_csv('nback_scores.csv', sep=',', index=False)