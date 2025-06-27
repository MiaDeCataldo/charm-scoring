# import framework (PANDAS) for manipulating data: https://pandas.pydata.org/
import pandas as pd
import glob
import re 


# read all matching file names in ./Flanker_csv folder
# this variable is a list of strings, all which are present and in form 'Flanker_csv/C2xxx_flanker*.csv'
files = glob.glob('Participant sub-folders/sub_C????/C????_flanker*.csv')

# create a dataframe with predefined columns to store results
results = pd.DataFrame(columns=['PID', 'flnk_con_rt', 'flnk_inc_rt', 'flnk_con_acc', 'flnk_inc_acc'])

# iterate through files that glob found
for f in files:
    
    print(f)
    # read data into dataframe from local file
    df = pd.read_csv(f)

    # names currently include directory; split string at '/' and take second half
    filename = re.split(r"[\\/]", f)[2]
    # 1. create list of characters from filename
    # 2. access list from the 1st index to the 4th index to find participant ID (skips C for filenames like C2xxx)
    # 3. resulting list is only integers that make up PID. Glue them together with empty string ('') to make one integer
    pid = ''.join(list(filename)[1:5])

    # only keep rows where column 'ItemID' contains 'FLANKER_FISH_TRIAL'
    # save dataset to new variable 'flanker_trials'
    flanker_trials = df[df['ItemID'].str.contains('FLANKER_FISH_TRIAL')]
    # now dataset only contains rows with 'FLANKER_FISH_TRIAL' in column 'ItemID';
    # we can now remove the text 'FLANKER_FISH_TRIAL' from this column, so that we're left with just a trial number (e.g. 1-30)
    flanker_trials.loc[: ,'ItemID'] = flanker_trials['ItemID'].map(lambda x: x.strip('FLANKER_FISH_TRIAL'))

    # define list that contains incongruent trial numbers
    inc_index = [3, 5, 7, 10, 13, 15, 17, 20, 24, 26]

    # trial numbers are considered 'strings' by the code right now (even though its just a digit)
    # we want to convert them to 'integers' so they can be compatible with number operations
    temp = pd.to_numeric(flanker_trials['ItemID'])
    flanker_trials.loc[ : ,'ItemID'] = temp

    # to filter for INCONGRUENT trials, this function is called to void rows that are CONGRUENT (we can then drop the voided rows)
    def zero_if_con(x):
      if x not in inc_index: return 0
      else: return x
    # same as above, but filters for CONGRUENT trials by voiding INCONGRUENT rows
    def zero_if_inc(x):
      if x not in inc_index: return x
      else: return 0

    # here, we are using the above functions as described to create two new dataframes: CON and INC
    incongruent = flanker_trials[flanker_trials['ItemID'].apply(zero_if_con) != 0]
    congruent = flanker_trials[flanker_trials['ItemID'].apply(zero_if_inc) != 0]

    # find reaction time (RT) for both INC and CON trials
    # format score to four decimal places
    response_time_con = congruent['ResponseTime'].mean()
    con_rt = '{:10.4f}'.format(response_time_con)

    response_time_inc = incongruent['ResponseTime'].mean()
    inc_rt = '{:10.4f}'.format(response_time_inc)

    # find accuracy (ACC) for both INC and CON trials
    # format score to four decimal places
    accuracy_con = congruent['Score'].sum() / len(congruent.index)
    con_acc = '{:10.4f}'.format(accuracy_con)

    accuracy_inc = incongruent['Score'].sum() / len(incongruent.index)
    inc_acc = '{:10.4f}'.format(accuracy_inc)

    # append participant data to end of output dataframe
    results.loc[len(results.index)] = [pid, con_rt, inc_rt, con_acc, inc_acc]
    

results = results.sort_values(by='PID')
# export output dataframe to local CSV file
results.to_csv('charm-scoring/flanker_scores.csv', sep=',', index=False)
