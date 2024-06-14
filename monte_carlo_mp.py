import numpy as np
from joblib import Parallel, delayed
from multiprocessing import cpu_count

def monte_carlo(curvnum,dc_obs,dc_train,train_size):
    dc_obs_rep = dc_obs[curvnum,:][None,...].repeat(train_size,axis=0)
    ind1 = np.argmin(mean_absolute_error(dc_obs_rep,dc_train,axis=1))
    return ind1

def monte_carlo_mp(dc_test,dc_train,train_size,ncurv):
    ind = Parallel(n_jobs=cpu_count())(delayed(monte_carlo)(i,dc_test,dc_train,train_size) for i in range(ncurv))
    return ind

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