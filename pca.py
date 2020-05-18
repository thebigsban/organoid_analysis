from read import *

# read in organoid ucsc data; rows = genes, columns = cells
a = read_organoid_ucsc()

# transpose to get to rows = cells, columns = genes
a = a.T
full_expr_mat = a

# sample approx 10% of the cells to perform PCA and/or tSNE
import numpy as np
import random
np.random.seed(0)
random.seed(0)
ndx = random.sample(range(200000), 20000)


expr_mat = full_expr_mat[ndx]



from sklearn.preprocessing import StandardScaler
expr_mat = StandardScaler().fit_transform(expr_mat)


from sklearn.decomposition import PCA
pca = PCA(n_components='mle', svd_solver = 'full')
principalComponents = pca.fit_transform(expr_mat)


principalComponents.shape

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(principalComponents[:,0], principalComponents[:,1], principalComponents[:,2])
plt.show()

