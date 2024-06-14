import numpy as np
from dc_fast import dc_fast

def getranges(dc,freq,E,nummode,vs2vp,wave,dvs):

    dc = np.squeeze(dc)
    lc = dc/freq
    lmin = np.min(lc)
    d_res = np.max(lc)/2
    
    d_min = []
    d_max = []
    i = 0
    d_temp = 0
    while d_temp<d_res:
        if i==0:
            d_min.append(lmin/3)
            d_max.append(lmin)
        elif i==1:
            d_min.append(d_max[i-1])
            d_max.append(d_min[i]+E*lmin)
        else:
            d_min.append(d_max[i-1])
            d_max.append(d_min[i]+E*(d_max[i-1]-d_min[i-1]))
        d_temp = d_max[-1]
        i+=1            
        
    if d_max[-1]>d_res:
        del d_max[-1]
        del d_min[-1]

    d_max = np.round(d_max,1)
    d_min = np.round(d_min,1)
    d_range = np.vstack(([d_min],[d_max]))
    
    
    thk_up = d_max-d_min
    thk_up[0] = d_max[0]
    thk_down = np.zeros(len(thk_up)) + np.round(lmin/3,1)
    
    lc = (dc/freq)*0.53
    vr2vs = 1.16
    dep_mean = np.mean(d_range,0)
    
    vs_mean = []
    for i in range(len(dep_mean)):
        vs_mean.append(vr2vs*dc[np.argmin(abs(lc-dep_mean[i]))])
    vs_mean.append(vr2vs*dc[0])
    vs_mean = np.int32(np.array(vs_mean))

    vs_up = vs_mean+dvs
    vs_down = vs_mean-dvs
    
    vs_diff = 50
    if np.where(vs_down<vs_diff)[0].size>0:
        vs_down[np.where(vs_down<vs_diff)[0]] = vs_diff

    for i in range(1,len(vs_down)):
        if vs_down[i] - vs_down[i-1] < vs_diff:
            vs_down[i] = vs_down[i-1] + vs_diff
            
    for i in range(len(vs_down)):
        if vs_up[i] <= vs_down[i]:
            vs_up[i] = vs_down[i] + vs_diff
    
#     if del1stlay:
#         thk_up = np.delete(thk_up,0,-1)
#         thk_down = np.delete(thk_down,0,-1)
#         vs_up = np.delete(vs_up,0,-1)
#         vs_down = np.delete(vs_down,0,-1)

    vp_down = np.int32(vs_down*vs2vp)
    vp_up = np.int32(vs_up*vs2vp)
    
    rho_down = np.int32(0.61*vp_down**0.18*1000)
    rho_up = np.int32(0.61*vp_up**0.18*1000)
    freq = np.atleast_2d(freq)
    dc_down = dc_fast(nummode,freq,vs_down,vp_down,rho_down,thk_up,wave=wave)
    dc_up = dc_fast(nummode,freq,vs_up,vp_up,rho_up,thk_down,wave=wave)
    
    range_model = {'vs_down':np.int32(vs_down),
                   'vs_up':np.int32(vs_up),
                   'thk_down':thk_down,
                   'thk_up':thk_up,
                   'vp_down':vp_down,
                   'vp_up':vp_up,
                   'rho_down':rho_down,
                   'rho_up':rho_up,
                   'dc_down':dc_down,
                   'dc_up':dc_up,
                   'd_range':d_range}
        
    return range_model


def getranges_mc(vs_rest_xi,thk_rest_xi,xi,freq,puasson=0.35,rho_const=1900,wave='rayleigh'):

    nummode = 1
    model_range = {}
    model_range['vs_down'] = np.min(vs_rest_xi[xi],axis=0)
    model_range['vs_up'] = np.max(vs_rest_xi[xi],axis=0)
    model_range['thk_down'] = np.min(thk_rest_xi[xi],axis=0)
    model_range['thk_up'] = np.max(thk_rest_xi[xi],axis=0)
    model_range['vp_down'] = np.int32(model_range['vs_down']*np.sqrt(2*(1-puasson)/(1-2*puasson)))
    model_range['vp_up'] = np.int32(model_range['vs_up']*np.sqrt(2*(1-puasson)/(1-2*puasson)))
    model_range['rho_down'] = np.int32(0.61*model_range['vp_down']**0.18*1000)
    model_range['rho_up'] = np.int32(0.61*model_range['vp_up']**0.18*1000)
    model_range['dc_down'] = dc_fast(nummode,freq,
                                     model_range['vs_down'],
                                     model_range['vp_down'],
                                     model_range['rho_down'],
                                     model_range['thk_up'],wave=wave)
    model_range['dc_up'] = dc_fast(nummode,freq,model_range['vs_up'],
                                   model_range['vp_up'],
                                   model_range['rho_up'],
                                   model_range['thk_down'],
                                   wave=wave)  
    return model_range



        
        