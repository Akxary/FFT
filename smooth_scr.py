import asyncio
import warnings
import aiofiles
import pandas as pd
import numpy as np
import math
import scipy as sc
import os


def sm_line(xm: np.array, cof: np.array, poly_degree: int) -> np.array:
    return np.array([sum([math.pow(x, poly_degree - j) * cof[j] for j in range(poly_degree + 1)]) for x in xm])


def main(file_name: str = '3 Gpa_405_50s_2sum_02mW.csv', n: int = 5, prominence: float = 0.1) -> ([], []):
    # read df, cut laser peak
    columns = ['N', 'l', 'I', 'Nan']
    df = pd.read_csv(f'D:\\Учёба\\нтц уп ран\\C60F\\raman_to_process\\{file_name}',
                     delimiter=',', header=None, skiprows=1, names=columns, decimal=',')
    df1 = df[['l', 'I']]
    df1 = df1.loc[df1['l'] > 500]
    # to de trend and normalize signal
    val1 = sc.signal.detrend(df1['I'])
    val1 = val1 / max(val1)
    peaks, properties = sc.signal.find_peaks(val1, width=5, prominence=prominence)
    properties['right_ips'] = list(map(lambda k: int(k) + 15, properties['right_ips']))
    properties['left_ips'] = list(map(lambda k: int(k) - 15, properties['left_ips']))
    dfv = pd.DataFrame(val1)
    dfv.columns = ['I']
    dfv['l'] = df1['l'].to_numpy()
    dfv_e = pd.DataFrame(columns=['I', 'l'])
    # cut peaks from df
    for i in range(len(peaks)):
        dfv_i = dfv.iloc[properties['left_ips'][i]:properties['right_ips'][i]]
        # adding cut peaks to new df
        dfv_e = dfv_e.append(dfv_i)
        # exclude peaks from signal data
        dfv = dfv[~dfv.isin(dfv_i)]
    # smooth signal without peaks
    dfv1 = dfv[dfv['l'].notna()]
    coefficient = np.polyfit(dfv1['l'], dfv1['I'], n)
    dfv['I'] = sm_line(dfv['l'], coefficient, n)
    # add peaks back
    l2, val2 = [], []
    for i in range(dfv.count()[0]):
        if np.isnan(dfv['l'][i]):
            l2.append(dfv_e['l'].loc[i])
            val2.append(dfv_e['I'].loc[i])
        else:
            l2.append(dfv['l'].loc[i])
            val2.append(dfv['I'].loc[i])
    return tuple(zip(l2, val2))


async def inout(file):
    res = main(file)
    print(f'start {file} writing')
    async with aiofiles.open('D:\\Учёба\\нтц уп ран\\C60F\\raman_to_process\\New_' + file,
                             'w', encoding='utf-8') as csvfile:
        await csvfile.writelines(('\t'.join((str(r[0]), str(r[1]), '\n')) for r in res))
    print(f'end {file} writing')


async def mega_main():
    await asyncio.gather(*(inout(fl) for fl in files))


files = filter(lambda f: '_full' not in f and 'mW.csv' in f and 'New_' not in f, os.listdir('D:\\Учёба\\нтц уп ран\\C60F\\raman_to_process'))

if __name__ == '__main__':
    warnings.filterwarnings(action='ignore', category=FutureWarning)
    asyncio.run(mega_main())
