
import pointCollection as pc
import numpy as np
import glob
import h5py
import re
import scipy.sparse as sp
import pandas as pd
import numpy as np
import argparse

from read_xovers import read_xovers
from filter_xovers import filter_xovers

def collect_xovers(xover_glob, bin_size=100e3, DEM=None, min_h=0,
                        min_r = 0,max_r=2.5e6,
                        max_delta_t=24*3600*10,
                        get_data=True,
                        verbose=False):
    tile_re=re.compile('E(.*)_N(.*).h5')

    pad_0=np.arange(-bin_size/2, bin_size/2*1.25, bin_size/4)
    x_pad, y_pad = np.meshgrid(pad_0, pad_0)
    v, d, m, D0, D1 = [[], [], [], [], []]
    files=[]
    for this_glob in xover_glob.split(' '):
        files += glob.glob(this_glob)

    if verbose:
        print(f"collect_xovers: for glob_str {xover_glob}, found {len(files)} files")

    xys=[]
    for file in files:
        try:
            xy=np.c_[[int(xx) for xx in tile_re.search(file).groups()]]
            if DEM is not None:
                zz = DEM.interp(xy[0]+x_pad.ravel(), xy[1]+y_pad.ravel())
                zz[~np.isfinite(zz)]=0
                if np.any(zz < min_h):
                    continue
            if min_r is not None:
                if np.all(np.sqrt((xy[0]+x_pad.ravel())**2+ (xy[1]+y_pad.ravel())**2)<min_r):
                    continue
            if max_r is not None:
                if np.all(np.sqrt((xy[0]+x_pad.ravel())**2+ (xy[1]+y_pad.ravel())**2)>max_r):
                    continue
            xys += [xy]

            vv, mm, DD = read_xovers(file)

            filter_xovers(vv, mm, DD, min_h=min_h)

            v += [vv]
            if get_data:
                D0 += [DD[0]]
                D1 += [DD[1]]
        except Exception as e:
            print(f"problem reading {file} :")
            print(e)
            pass

    v=pc.data(columns=2).from_list(v)

    if get_data:
        D0=pc.data(columns=2).from_list(D0)
        D1=pc.data(columns=2).from_list(D1)
        return v, D0, D1
    else:
        return v
