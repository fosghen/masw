import numpy as np

def monte_carlo(dc_obs,dc_train):
    dc_obs_rep = np.squeeze(dc_obs)[None,...].repeat(np.size(dc_train,0),axis=0)
    ind1 = np.argmin(mean_squared_error(dc_obs_rep,dc_train,axis=1))
    return ind1

def mean_absolute_percentage_error(y_true, y_pred, axis=(0,1)):
    return (np.mean(np.abs((y_true - y_pred) / y_true), axis)) * 100

def max_absolute_error(y_true, y_pred, axis=(0,1)):
    return np.max(np.abs(y_true - y_pred),axis)

def mean_absolute_error(y_true, y_pred, axis=(0,1)):
    return np.mean(np.abs(y_true - y_pred),axis)
    
def mean_squared_error(y_true, y_pred, axis=(0,1)):
    return np.mean(np.abs((y_true - y_pred)**2),axis)

def root_mean_squared_error(y_true, y_pred, axis=(0,1)):
    return np.sqrt(mean_squared_error(y_true, y_pred, axis))

def weighted_mean_absolute_percentage_error(y_true, y_pred, axis=(0,1)):
    return np.sum(abs(y_true-y_pred),axis=axis)/np.sum(abs(y_true),axis=axis)*100