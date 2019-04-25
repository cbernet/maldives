import numpy as np
import matplotlib.pyplot as plt

linx = np.arange(-4, 4, 0.1)
plt.plot(linx, linx)
plt.plot(linx, linx/linx)
plt.savefig('x.png')
plt.show()
plt.clf()
plt.plot(linx, linx**2)
plt.plot(linx, 2*linx)
plt.savefig('x2.png')
plt.show()

