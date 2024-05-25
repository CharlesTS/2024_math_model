import pandas as pd

file_name = ['问题1：（1）A.csv', '问题1：（1）B.csv', '问题1：（1）C.csv']

for i in range(len(file_name)):
    data = pd.read_csv(file_name[i])
    data = data.dropna()
    win = data['风电购电量']
    light = data['光伏购电量']
    buy = data['电网购电量']
    drop = data['弃风弃光电量']
    total = win+light+buy-drop
    print(sum(drop))
    print(sum(buy))