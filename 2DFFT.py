import numpy as np
import matplotlib.pyplot as plt

n = 1
theta = np.arange(-n * np.pi, n * np.pi, np.pi / 100)
theta, phi = np.meshgrid(theta, theta)
z = np.sin(theta) + 2 * np.sin(5 * phi) + 3 * np.sin(2 * theta) + 4 * np.sin(phi)
# z = np.sin(theta)
ftz = np.abs(np.fft.fftshift(np.fft.fft2(z)))
ftz = ftz / np.max(ftz)
fig = plt.figure(dpi=300)
ax1 = fig.add_subplot(121)
ext1 = np.min(theta), np.max(theta), np.min(theta), np.max(theta)
img1 = ax1.imshow(z, extent=ext1, cmap='Accent_r')
fig.colorbar(mappable=img1)
ax2 = fig.add_subplot(122)
ftfreq1 = np.fft.fftfreq(z.shape[0])
ftfreq2 = np.fft.fftfreq(z.shape[0])
# ftz = np.ma.masked_where(ftz < 0.1, ftz)
ext2 = np.min(ftfreq1), np.max(ftfreq1), np.min(ftfreq2), np.max(ftfreq2)
img2 = ax2.imshow(ftz, extent=ext2, cmap='CMRmap_r')
plt.colorbar(mappable=img2)
plt.tight_layout()
plt.show()
