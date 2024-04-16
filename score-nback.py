import pandas as pd
import glob

# read all matching file names in ./NBack_csv folder
files = glob.glob('NBack_csv/C2???_DualNBack_Task_*.csv')

results = pd.DataFrame(columns=['PID', '1B_AVG_CORR_RT', '1B_AVG_INCORR_RT', '1B_ACC', '2B_AVG_CORR_RT', '2B_AVG_INCORR_RT', '2B_ACC',])

for f in files:
    
    df = pd.read_csv(f)
    df.dropna()

    print(f)

    filename = f.split('/')[1]
    pid = ''.join(list(filename)[1:5])


    oneback_avg_corr_rt = df['oneback_avg_corr'].dropna()
    if (len(oneback_avg_corr_rt.index) < 1): oneback_avg_corr_rt = None
    else: oneback_avg_corr_rt = oneback_avg_corr_rt.iloc[0]

    oneback_avg_incorr_rt = df['oneback_avg_incorr'].dropna()
    if (len(oneback_avg_incorr_rt.index) < 1): oneback_avg_incorr_rt = None
    else: oneback_avg_incorr_rt = oneback_avg_incorr_rt.iloc[0]

    oneback_acc = df['oneback_corr'].dropna()
    if (len(oneback_acc.index) < 1): oneback_acc = None
    else: oneback_acc = oneback_acc.iloc[0]

    twoback_avg_corr_rt = df['twoback_avg_corr'].dropna()
    if (len(twoback_avg_corr_rt.index) < 1): twoback_avg_corr_rt = None
    else: twoback_avg_corr_rt = twoback_avg_corr_rt.iloc[0]

    twoback_avg_incorr_rt = df['twoback_avg_incorr'].dropna()
    if (len(twoback_avg_incorr_rt.index) < 1): twoback_avg_incorr_rt = None
    else: twoback_avg_incorr_rt = twoback_avg_incorr_rt.iloc[0]

    twoback_acc = df['twoback_corr'].dropna()
    if (len(twoback_acc.index) < 1): twoback_acc = None
    else: twoback_acc = twoback_acc.iloc[0]


    results.loc[len(results.index)] = [pid, oneback_avg_corr_rt, oneback_avg_incorr_rt, oneback_acc, twoback_avg_corr_rt, twoback_avg_incorr_rt, twoback_acc]

results.to_csv('nback_scores.csv', sep=',', index=False)