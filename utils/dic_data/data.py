# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 21:30:38 2018

@author: gidelang
"""

import os
import time
import numpy as np
import pickle
DATAPATH = r'D:\data'

def current_date():
    ts = time.localtime()
    datestr = '%4d%02d%02d'%(ts.tm_year,
                                  ts.tm_mon,
                                  ts.tm_mday)
    return datestr

def current_time():
    ts = time.localtime()
    timestr = '%02d%02d%02d'%(ts.tm_hour,
                                  ts.tm_min,
                                  ts.tm_sec)
    return timestr
    

def generate_datetime():
    ts = time.localtime()
    tag = current_date() + '_' + current_time()
    return tag

def create_datafolder(datapath = DATAPATH):
    
    fol = os.path.join(datapath, current_date())
    if not os.path.exists(fol):
        os.mkdir(fol)
    return fol

def create_filepath(datapath = DATAPATH):
    basepath = os.path.join(create_datafolder(datapath), current_date() )
    kk = 0
    exists = True
    while exists:
        kk+=1
        testpath = basepath + '_%03d'%kk
        pickle_exists = os.path.exists(testpath + '.pickle')
        hdf5_exists = os.path.exists(testpath + '.hdf5')
        dat_exists = os.path.exists(testpath + '.dat')
        exists = dat_exists or hdf5_exists or pickle_exists
    return testpath

#find_data

def find_data(datetstr, basedatdir = r'd:\data', dtype = 'hdf5'):
    datestr, timestr = datetstr.split('_')
    basedir = os.path.join(basedatdir, datestr)
    dirlist = os.listdir(basedir)
    for dirstr in dirlist:
        if dirstr.find(timestr) > -1:
            datdir = os.path.join(basedir, dirstr)
            print('found data: ', datdir)
            break
    dpath = os.path.join(datdir, datestr + '_' + dirstr + '.' + dtype)
    return dpath 
    
def get_last_data_file(datapath = DATAPATH):
    ls = os.listdir(create_datafolder(datapath))
    ls.sort()
    return open(os.path.join(create_datafolder(datapath), ls[-1]), 'rb')

def init_single_trace(xnames, ynames, npoints):
    data_trace = {}
    if type(xnames) != type([]):
        xnames = [xnames]
    ncoords = len(xnames)
    if type(ynames) != type([]):
        ynames = [ynames]
    nvals = len(ynames)
    for kk, xname in enumerate(xnames):
           data_trace['xname%01d'%kk]= xname
    for kk, yname in enumerate(ynames):
           data_trace['yname%01d'%kk]= yname
          
    data_trace['vals'] = np.zeros([npoints, ncoords + nvals])
    return data_trace 
    
def init_dic_data(name, datapath = DATAPATH):
    fpath = create_filepath(datapath)
    dat = {'filepath': fpath,
           'timestamp': generate_datetime(),
           'name' : name
           }
    return dat    
    

def save_data_pickle(dat):
    pickle.dump(dat, open(dat['filepath']+'.pickle', 'wb'))    
def open_last_pickle(datapath = DATAPATH):
    return pickle.load(get_last_data_file(datapath))    
    