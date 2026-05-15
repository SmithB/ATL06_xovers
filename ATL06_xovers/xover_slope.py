import numpy as np

def xover_slope(d0, d1):

    x=np.c_[d0.x, d1.x]
    y=np.c_[d0.y, d1.y]
    z=np.c_[d0.h_li, d1.h_li]
    dx = x-np.mean(x, axis=1)
    dy = y=np.mean(y, axis=1)

    ones4 = np.ones(4)
    dzdx = np.ones(x.shape[0])
    dzdy = np.ones(x.shape[0])
    for row in x.shape[0]:
        G=np.c_[dx[row,:], dy[row,:], ones4]
        m=np.linalg.solve(G.T@G, G.T@z[row,:])
        dzdx[row]=m[0]
        dzdy[row]=m[1]

    return dzdx, dzdy