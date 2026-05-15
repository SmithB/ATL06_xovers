import numpy as np

def filter_xovers(v, m, data,
                  slope_max = 0.25, grounded_tol = 0.99,
                max_delta_t = None,
                  min_h=None):
    '''
    Filter the crossovers based on field values
    '''
    #print( f"grounded_fraction: {np.nanmean(m.grounded):2.2f}")
    good=np.all(v.atl06_quality_summary < 0.01, axis=1)
    for di in data:
        good &= np.abs(di.delta_time[:,1]-di.delta_time[:,0]) < 0.005
    #good &= m.grounded > grounded_tol
    if slope_max is not None:
        good &= np.all(np.abs(np.c_[v.dh_fit_dx, v.dh_fit_dy])< slope_max, axis=1)

    if max_delta_t is not None:
        good &= (v.delta_t[:,1]-v.delta_t[:,0]) < max_delta_t
    if min_h is not None:
        good &= (np.all(v.h_li > min_h, axis=1))

    v.index(good)
    m.index(good)
    for di in data:
        di.index(good)
