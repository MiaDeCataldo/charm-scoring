# the goal of this code is to extract accuracy and reaction time scores for both 1Back and 2Back tasks, only considering task relavant data
# for this code to run properly, there should be a folder named "NBack_csv" containing output PsyhcoPy NBack .csv files, all named with "C2xxx_DualNBack_Task_...csv" format
# PANDAS should be installed to a virtual environment before running the code. This can be done by using the commands: 
#   1. "python3 -m venv .venv" 2. "source .venv/bin/activate" 3. "pip install pandas"
# it can be ran with "python score-nback.py" or "python3 score-nback.py", whichever python version is installed on your computer

# import external libraries
import pandas as pd # for dataframe creation and manipulation
import glob # for finding files whose paths match a pattern
import re 
from datetime import datetime

#  create list of file names (found in NBack_csv)
files = glob.glob('CHARM sub Folders/sub_C????/C????_DualNBack_Task_*.csv')

# create output dataframe (with specified column names)
results = pd.DataFrame(columns=['PID', 'nb1_avg_crct', 'nb1_avg_inc', 'nb1_accrcy', 'nb2_avg_crct', 'nb2_avg_inc', 'nb2_accrcy'])

# for each file in "files" list, execute the indented code:
for f in files:

  print(f) 
  # function from Panda's library: create dataframe from path to CSV
  data_csv = pd.read_csv(f)

  # turn "Participant sub-folders/sub_C????/C????_DualNBack_Task_*.csv" into "C????_DualNBack_Task_*.csv"
  filename = re.split(r"[\\/]", f)[2]
  # extract xxxx from the filename found above (turn it back into a string)
  pid = ''.join(list(filename)[1:5])

  # list of relavant column names within data_csv
  columns = ['CorrResp', 'oneback_resp.corr', 'oneback_resp.rt', 'key_resp_2back.corr', 'key_resp_2back.rt']
  # same list as above, minus the first column
  rel_col = columns[1:]

  # access data_csv at all of the "columns": then drop all rows where "rel_col"s are N/A (save that view of dataframe to "relavant")
  relavant = data_csv[columns].dropna(how='all', subset=rel_col)

  # create new view based on "relavent": focus on rows that are task relavant (ignore NoBack responses - "w" and "None")
  taskrelavant = relavant[(~relavant['CorrResp'].str.contains('w', na=False)) & (relavant['CorrResp'].isna() == False)]

  # extract 1Back and 2Back accuracy from respective columns
  acc1Back = taskrelavant['oneback_resp.corr'].mean()
  acc2Back = taskrelavant['key_resp_2back.corr'].mean()


  # create new views for 1Back: separate correct and incorrect responses
  corr1Back = taskrelavant[taskrelavant['oneback_resp.corr'] == 1]
  incorr1Back = taskrelavant[taskrelavant['oneback_resp.corr'] == 0]

  # find correct/incorrect reaction times for 1Back by averaging respective RT columns within new 1B views
  rt1BackCorr = corr1Back['oneback_resp.rt'].mean()
  rt1BackIncorr = incorr1Back['oneback_resp.rt'].mean()


  # create new views for 2Back: separate correct and incorrect responses
  corr2Back = taskrelavant[taskrelavant['key_resp_2back.corr'] == 1]
  incorr2Back = taskrelavant[taskrelavant['key_resp_2back.corr'] == 0]

  # find correct/incorrect reaction times for 2Back by averaging respective RT columns within new 2B views
  rt2BackCorr = corr2Back['key_resp_2back.rt'].mean()
  rt2BackIncorr = incorr2Back['key_resp_2back.rt'].mean()

  # insert new row, containing participant results, into "result" dataframe (order of values same as when we created df originally)
  results.loc[len(results.index)] = [pid, rt1BackCorr, rt1BackIncorr, acc1Back, rt2BackCorr, rt2BackIncorr, acc2Back]
# (loop ends here: move on to next file in list until all files have been read)


# sort "results" by participant ID
results = results.sort_values(by='PID')
# export output dataframe to local CSV file
results.to_csv('charm-scoring/nback_scores'+datetime.today().strftime('%m%d%Y')+'.csv', sep=',', index=False)
