import pandas as pd
import glob
import math

files = glob.glob('NBack_csv/C2???_DualNBack_Task_*.csv')

results = pd.DataFrame(columns=['PID', '1B_AVG_CORR_RT', '1B_AVG_INCORR_RT', '1B_ACC', '2B_AVG_CORR_RT', '2B_AVG_INCORR_RT', '2B_ACC'])

for f in files:

  df = pd.read_csv(f)

  filename = f.split('/')[1]
  pid = ''.join(list(filename)[1:5])

  columns = ['CorrResp', 'oneback_resp.corr', 'oneback_resp.rt', 'key_resp_2back.corr', 'key_resp_2back.rt']
  rel_col = columns[1:]

  relavant = df[columns].dropna(how='all', subset=rel_col)

  #taskrelavant = relavant[(relavant['CorrResp'] != 'w') & (relavant['CorrResp'] != None)]

  #taskrelavant = relavant[~relavant['CorrResp'].str.contains('w', na=False)]

  taskrelavant = relavant[(~relavant['CorrResp'].str.contains('w', na=False)) & (relavant['CorrResp'].isna() == False)]

  Acc1Back = taskrelavant['oneback_resp.corr'].mean()
  Acc2Back = taskrelavant['key_resp_2back.corr'].mean()


  Corr1Back = taskrelavant[taskrelavant['oneback_resp.corr'] == 1]

  Incorr1Back = taskrelavant[taskrelavant['oneback_resp.corr'] == 0]

  Corr2Back = taskrelavant[taskrelavant['key_resp_2back.corr'] == 1]

  Incorr2Back = taskrelavant[taskrelavant['key_resp_2back.corr'] == 0]


  RT1BackCorr = Corr1Back['oneback_resp.rt'].mean()
  RT1BackIncorr = Incorr1Back['oneback_resp.rt'].mean()

  RT2BackCorr = Corr2Back['key_resp_2back.rt'].mean()
  RT2BackIncorr = Incorr2Back['key_resp_2back.rt'].mean()






  results.loc[len(results.index)] = [pid, RT1BackCorr, RT1BackIncorr, Acc1Back, RT2BackCorr, RT2BackIncorr, Acc2Back]

  #print(RT1BackCorr, RT1BackIncorr, Acc1Back, RT2BackCorr, RT2BackIncorr, Acc2Back)


results = results.sort_values(by='PID')
# export output dataframe to local CSV file
results.to_csv('nback_scores.csv', sep=',', index=False)
