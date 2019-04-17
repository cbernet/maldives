import numpy as np
import matplotlib.pyplot as plt

values = [1.1, 1.5, 2.2, 3.5, 3.5, 3.6, 4.1]
weights = [1., 1., 3., 1.2, 1.4, 1.1, 0.2]
plt.hist(values, bins=4, range=(1,5), weights=weights)
plt.show()




