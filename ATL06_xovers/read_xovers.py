import pointCollection as pc
import numpy as np
import glob
import h5py
import re
import scipy.sparse as sp
import pandas as pd
import argparse
import numpy as np

def read_xovers(file, fields=None, get_data=False):
    '''
    Read crossovers from a saved crossover file

    Inputs :
    File (str): hdf-5 file to read
    fields (list of strs): fields to read from the file

    Returns:
    v (pc.data) field values interpolated to the crossover location
    m (pc.data) Metadata fields for each crossover location, including grounded status, slope, and location
    data (list of pc.data objects) raw data read from each crossover file
    '''

    if fields is None:
        fields=['x','y','delta_time','h_li','h_li_sigma','h_mean','spot', 'rgt', 
                'dh_fit_dx','dh_fit_dy','atl06_quality_summary', 'latitude',
                'seg_azimuth','ref_azimuth','ref_coelv', 'cycle_number']

    m = pc.data().from_h5(file, field_dict={None:['grounded','x','y','slope_x','slope_y']})
    v=pc.data(columns=2)
    data = [pc.data(columns=2).from_h5(file, field_dict={group:fields+['W']}) for group in ['data_0','data_1']]
    d=pc.data()
    for field in fields:
        if field=='W':
            continue
        temp = np.zeros((m.size, 2))
        for col in [0, 1]:
            temp[:, col] = np.sum(data[col].W * getattr(data[col], field), axis=1)

        if field in ['rgt','cycle','spot']:
            # integer fields:
            v.assign({ field : np.round(temp).astype(int)})
        else:
            v.assign({ field : temp})

    for item in [v, d]:
        item.__update_size_and_shape__()

    return v, m, data
