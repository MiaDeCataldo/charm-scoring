# import framework (PANDAS) for manipulating data
import pandas as pd

# participant ID
id = 2000

# create a dataframe with predefined columns to store results
results = pd.DataFrame(columns=['PID', 'CON_RT', 'INC_RT', 'CON_ACC', 'INC_ACC'])

# create a loop: execute indented code for all found participant IDs
while id <= 2999:

  # try to run the following indented code: in case there are any errors, don't crash, but jump to 'except' instead
  try:

    # call predefined Pandas function to read CSV file 
    # MUST be in Flanker_csv directory/folder and named as C2xxx_flanker.csv
    # read dataframe into 'df' variable
    df = pd.read_csv(f'Flanker_csv/C{id}_flanker.csv')

    # display to terminal the first 5 rows of data (display first x rows with .head(x))
    print(df.head())

    # clean up data: get rid of unnecessary columns and save trimmed down dataset to a new variable 'flanker_scoring'
    flanker_scoring = df.drop([
      'PID', 
      'RegistrationID', 
      'AssessmentName', 
      'InstrumentID', 
      'InstrumentName', 
      'ThetaStandardError', 
      'Theta', 
      'TScore', 
      'TScoreStandardError', 
      'DateCreated', 
      'NumberFormatting'
      ], axis=1) #axis=1 means index the COLUMNS, not rows

    # continue cleanup: only keep rows where column 'ItemID' contains 'FLANKER_FISH_TRIAL'
    # save dataset to new variable 'flanker_trials'
    flanker_trials = flanker_scoring[flanker_scoring['ItemID'].str.contains('FLANKER_FISH_TRIAL')]
    # now dataset only contains rows with 'FLANKER_FISH_TRIAL' in column 'ItemID';
    # we can now remove the text 'FLANKER_FISH_TRIAL' from this column, so that we're left with just a trial number (e.g. 1-30)
    flanker_trials.loc[: ,'ItemID'] = flanker_trials['ItemID'].map(lambda x: x.strip('FLANKER_FISH_TRIAL'))

    print(id)
    print(flanker_trials)

    # define list that contains incongruent trial numbers
    inc_index = [3, 5, 7, 10, 13, 15, 17, 20, 24, 26]
    # incongruent (INC) 10 Trials: 3, 5, 7, 10, 13, 15, 17, 20, 24, 26
    # congruent (CON) 20 Trials: !INC (not incongruent trials)

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

    # write to file, using file variable 'scoring_file' opened at beginning
    pid = f'{id}'

    # find reaction time (RT) for both INC and CON trials
    # format score to four decimal places
    response_time_con = congruent['ResponseTime'].mean()
    con_rt = '{:10.4f}'.format(response_time_con)

    response_time_inc = incongruent['ResponseTime'].mean()
    inc_rt = '{:10.4f}'.format(response_time_inc)

    # find accuracy (ACC) for both INC and CON trials
    # format score to four decimal places
    accuracy_con = congruent['Score'].sum() / len(congruent)
    con_acc = '{:10.4f}'.format(accuracy_con)

    accuracy_inc = incongruent['Score'].sum() / len(incongruent)
    inc_acc = '{:10.4f}'.format(accuracy_inc)

    # append participant data to end of output dataframe
    results.loc[len(results.index)] = [pid, con_rt, inc_rt, con_acc, inc_acc]

  # only gets run whenever 'try' block fails (file name does not exist); go to next ID
  except:
    pass
  

  # necessary for 'while' loop to advance to next participant ID
  id += 1

# export compiled dataframe to a .csv file
results.to_csv('scoring_file.csv', sep='\t')