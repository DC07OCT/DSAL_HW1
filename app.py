if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--training',default='training_data.csv',help='input training data file name.')
    parser.add_argument('--output',default='submission.csv',help='output file name')
    args=parser.parse_args()

    import pandas as pd# pip install pandas
    import numpy as np
    from pandas import read_csv
    # read the csv file()
    import csv
    import statistics


    path = 'C://Users/周郁庭/Desktop/DSAI_HW1_Electricity forecast/Trainingdata_new_2.csv'
    # df = read_csv(path, encoding='gb2312')
    df = read_csv(path, header=0, encoding='gb18030', usecols=[0, 3, 4, 5, 6, 9, 10, 11, 12, 15, 16, 17],
                  parse_dates=[0])  # ,encoding='gb18030'如果檔名中有中文
    df.columns = ['2021Date', '2021PowerSupply', '2021peakpower', '2021operate reserve', '2020Date', '2020PowerSupply',
                  '2020peakpower', '2020operate reserve', '2019Date', '2019PowerSupply', '2019peakpower',
                  '2019operate reserve']  # ,'Operating Reserve Ratio(%)'
    print(df.shape)
    print(df)
    # print(df['2021Date'][0])#2021-01-01 00:00:00
    print(df['2020Date'][74])  # excel-76col
    num = 94
    diff_PS = 0
    for i in range(94):
        if np.isnan(df['2020PowerSupply'][i]) or np.isnan(df['2019PowerSupply'][i]):
            num = num - 1
        else:
            diff_PS = diff_PS + (df['2020PowerSupply'][i] - df['2019PowerSupply'][i])
    print('diff_PS', diff_PS)
    avgdiff_PS = diff_PS / num
    print(num)
    print(avgdiff_PS)  # 1835.1

    for i in range(31, 94):
        if not np.isnan(df['2020PowerSupply'][i]):
            df['2021PowerSupply'][i] = df['2020PowerSupply'][i] + avgdiff_PS

    print(df['2021Date'][31])
    print(df['2021PowerSupply'].iloc[31:50])
    print(df['2021PowerSupply'].iloc[50:94])

    for i in range(31, 80):
        if not np.isnan(df['2021PowerSupply'][i]):
            df['2021peakpower'][i] = df['2021PowerSupply'][i] - df['2021operate reserve'][i]

    print(df['2021peakpower'].iloc[31:50])
    print(df['2021peakpower'].iloc[50:80])
    num = 81
    sum_PP_predict = 0

    for i in range(81):
        if np.isnan(df['2021peakpower'][i]) or np.isnan(df['2020peakpower'][i]):
            num = num - 1
        else:
            sum_PP_predict = sum_PP_predict + (df['2021peakpower'][i] - df['2020peakpower'][i])
            print(df['2021peakpower'][i] - df['2020peakpower'][i])
    print('above')
    sum_PP_pred = sum_PP_predict / num

    print(num)
    print(sum_PP_pred)  # 2082.2725806451635

    # 預測20210322~end 尖峰負載
    print(df['2021Date'][80])
    for i in range(80, 94):
        if not np.isnan(df['2020peakpower'][i]) and not np.isnan(df['2019peakpower'][i]):
            df['2021peakpower'][i] = df['2020peakpower'][i] + (
                        df['2020peakpower'][i] - df['2019peakpower'][i] + sum_PP_pred) / 2
            print(df['2020peakpower'][i] - df['2019peakpower'][i])

    print(df['2021peakpower'])

    # 預測20210322~end 備轉容量
    for i in range(80, 94):
        if not np.isnan(df['2021peakpower'][i]) and not np.isnan(df['2021PowerSupply'][i]):
            df['2021operate reserve'][i] = df['2021PowerSupply'][i] - df['2021peakpower'][i]

    print(df['2021operate reserve'])

    # 手動修改(PP感覺怪怪)
    for i in range(81, 87):
        df['2021operate reserve'][i] = (df['2021operate reserve'][i] + df['2021operate reserve'][i - 7]) / 2

    # submisssion
    print(df['2021Date'].iloc[81:88])
    print(df['2021operate reserve'].iloc[81:88])

    # 寫入csv file
    with open('submission.csv', 'w', newline="") as new_file:
        writer = csv.writer(new_file)
        writer.writerow(['date', 'operating_reserve(MV)'])
        for i in range(81, 88):
            writer.writerow(['202102%s' % (i - 58), df['2021operate reserve'][i]])
