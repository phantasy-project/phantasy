#!/usr/bin/python

#
# test dist
#
# Tong Zhang <zhangt@frib.msu.edu>
# 2017-03-28 16:14:10 PM EDT
#

import numpy as np


mean1 = [0, 0]
cov1 = [[0.01, 0], [0, 0.04]]
N1 = 5000
x1, y1 = np.random.multivariate_normal(mean1, cov1, N1).T

mean2 = [0.2, 0.2]
cov2 = [[0.0025, 0.001], [0.001, 0.0055]]
N2 = 5000
x2, y2 = np.random.multivariate_normal(mean2, cov2, N2).T

mean3 = [0.4, 0.6]
cov3 = [[0.0035, 0.001], [0.001, 0.0095]]
N3 = 5000
x3, y3 = np.random.multivariate_normal(mean3, cov3, N3).T
#
import matplotlib.pyplot as plt

bd = 2
fig = plt.figure(1)
ax = fig.add_subplot(111, aspect='equal', xlim=[-bd,bd], ylim=[-bd,bd])
ax.plot(x1, y1, '.', color='r', ms=1, label='1')
ax.plot(x2, y2, '.', color='b', ms=1, label='2')
ax.plot(x3, y3, '.', color='g', ms=1, label='3')
ax.legend()

#
x, y = np.concatenate([x1, x2, x3]), np.concatenate([y1, y2, y3])
new_fig = plt.figure(2, figsize=(10,8), dpi=200)
new_ax = new_fig.add_subplot(111, aspect='equal', xlim=[-bd,bd], ylim=[-bd,bd])
new_ax.plot(x, y, '.', color='r', ms=0.2)

hist_x, edge_x = np.histogram(x, range=[-bd,bd], bins=100, density=True)
hist_y, edge_y = np.histogram(y, range=[-bd,bd], bins=100, density=True)
ex = (edge_x[0:-1:1] + edge_x[1::1])/2
ey = (edge_y[0:-1:1] + edge_y[1::1])/2
new_ax.plot(ex, hist_x/2-bd, '--k', alpha=0.5, lw=1.0)
new_ax.plot(hist_y/2-bd, ey, '--k', alpha=0.5, lw=1.0)

plt.show()

np.savetxt('dist.dat', np.vstack([x, y]))
