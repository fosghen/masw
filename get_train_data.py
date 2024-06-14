import numpy as np
from dc_fast import dc_fast_par
import json
import pickle

def gettraindata(model_range,freq,nummode,ncurv,vs2vp,wave):
    
    nlay = max(np.shape(model_range['vs_down']))
    
    vs_train = np.zeros((ncurv,nlay))
    thk_train = np.zeros((ncurv,nlay-1))
    for i in range(nlay):
        vs_train[:,i] = np.random.randint(model_range['vs_up'][i]-model_range['vs_down'][i],size=ncurv) + model_range['vs_down'][i]

    for i in range(nlay-1):
        thk_train[:,i] = np.round((model_range['thk_up'][i]-model_range['thk_down'][i])*np.random.rand(ncurv) + model_range['thk_down'][i],1)

    vs_train = np.int32(vs_train)
    vp = np.int32(vs_train*vs2vp)
    rho = np.int32(0.61*vp**0.18*1000)    
    dc_train = dc_fast_par(nummode,freq,vs_train,vp,rho,thk_train,ncurv,wave=wave)
    
    ind_row_nan = np.unique(np.where(np.isnan(dc_train) == True)[0])
    dc_train_clear = np.delete(dc_train,ind_row_nan,axis=0)
    vs_train_clear = np.delete(vs_train,ind_row_nan,axis=0)
    thk_train_clear = np.delete(thk_train,ind_row_nan,axis=0)
            
    dc_train_all_sec_modes = []
    for ii in range(nummode):
        dc_train_all_sec_modes.extend(list(np.squeeze(dc_train_clear[:,:,ii].T)))
    dc_train_all_sec_modes = np.array(dc_train_all_sec_modes).T

    return dc_train_all_sec_modes, vs_train_clear, thk_train_clear

def load_train_data(datafile):
    b_file = open(datafile+'.pkl', "rb")
    data = pickle.load(b_file)
    b_file.close()
    return np.array(data['dc_train']), np.array(data['vs_train']), np.array(data['thk_train'])

def save_train_data(data,filename):
    f = open(filename+".pkl", "wb")
    pickle.dump(data, f)
    f.close()
    return