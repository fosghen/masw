import numpy as np

def seiswindow(data,percdecay=10):
    
    nt = np.max(np.shape(data))
    nx = np.min(np.shape(data))
    smooth_t = int(np.floor(nt*percdecay/100))
    smooth_x = int(np.floor(nx*percdecay/100))
    
    x_window = np.zeros((1,nx)) 
    t_window = np.zeros((1,nt)) 
    window = np.zeros((np.shape(data)))

    t_left_side = [(-np.cos(np.linspace(0.01,np.pi,smooth_t))+1)/2]
    t_centr = np.ones((1,nt-2*smooth_t))
    t_right_side = np.fliplr(t_left_side)
    t_window = np.concatenate((t_left_side,t_centr,t_right_side),axis=1)

    x_left_side = [(-np.cos(np.linspace(0.01,np.pi,smooth_x))+1)/2]
    x_centr = np.ones((1,nx-2*smooth_x))
    x_right_side = np.fliplr(x_left_side)
    x_window = np.concatenate((x_left_side,x_centr,x_right_side),axis=1)
    
    window = x_window*t_window.T
    
    return window