import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# read spectra from CSV
columns = ['N', 'l', 'I', 'Nan']
df = pd.read_csv('D:\\Учёба\\нтц уп ран\\C60F\\raman_to_process\\3 Gpa_405_50s_2sum_02mW.csv',
                 delimiter=',', header=None, skiprows=1, names=columns, decimal=',')
# cut lambda < 500 and useless columns
df1 = df[['l', 'I']]
df1 = df1.loc[df1['l'] > 500]
# spline spectra (get coefficient)
n = 3
df2 = df1.query('l<1000 or l>2000')
cof = np.polyfit(df2['l'], df2['I'], n)
# spline spectra
df3 = pd.DataFrame()
df3['I'] = df1['I'] - [sum([math.pow(x, n - i) * cof[i] for i in range(n + 1)]) for x in df1['l']]
df3['l'] = df1['l']
# make spectra shape to calc frequencies
val4 = np.array(df3.iloc[400:700]['I'])
val5 = np.append(val4, val4)
val5 = np.append(val5, val4[:149])
# calc frequencies to subtract
ampl = np.fft.fft(val5)
frq = np.fft.fftfreq(ampl.shape[0])
# get frequencies positions
center = frq[np.argmax(np.abs(ampl))]
bord: float = 0.01
u_b, l_b = center + bord, center - bord
ampl1 = np.where(((frq < l_b) + (frq > u_b)) * ((frq > -l_b) + (frq < -u_b)), ampl, np.zeros(749))
# spec fourier transform
sp_ampl = np.fft.fft(df3['I'])
sp_frq = np.fft.fftfreq(sp_ampl.shape[0])
sp_tfr = np.array([sp_frq, sp_ampl])
# correction
sp_ampl_corr = np.where(((sp_tfr[0] < l_b) + (sp_tfr[0] > u_b)) * ((sp_tfr[0] > -l_b) + (sp_tfr[0] < -u_b)),
                        sp_tfr, np.array([frq, np.zeros(749)]))
# inverse transform
corr_signal = np.fft.ifft(sp_ampl_corr[1])
# plot the result
fig1, ax = plt.subplots(2, 2, figsize=(12, 12))
ax[0, 0].plot(frq, ampl)
ax[0, 1].plot(frq, ampl1)
ax[1, 0].plot(df3['l'], df3['I'])
ax[1, 1].plot(df3['l'], corr_signal)
plt.show()
