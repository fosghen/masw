from disba import PhaseDispersion
import numpy as np
from joblib import Parallel, delayed
from multiprocessing import cpu_count

def dc_fast(nummode,f,vs,vp,rho,thk,wave='rayleigh'):    
    velocity_model = np.vstack((np.atleast_2d(np.hstack((np.squeeze(thk),0))),
                                np.atleast_2d(vp),
                                np.atleast_2d(vs),
                                np.atleast_2d(rho)))
    velocity_model = velocity_model/1000
    t = np.sort(1/np.squeeze(f))
    nf = len(np.squeeze(f))
    dc = np.zeros((nf,nummode))
    try:
        pd = PhaseDispersion(*velocity_model,dc=0.00005)
        for ii in range(nummode):
            cpr = pd(t,mode=ii,wave=wave).velocity
            dc[nf-len(cpr):,ii] = cpr[::-1]*1000
    except:
        dc[:] = 0  
    return dc

def dc_fast_par(nummode,f,vs,vp,rho,thk,ncurv,wave='rayleigh'):
    dc_mp = Parallel(n_jobs=cpu_count())(delayed(dc_fast_for_par)(nummode,f,vs[i],vp[i],rho[i],thk[i],wave=wave) for i in range(ncurv))
    return np.array(dc_mp)


def dc_fast_for_par(nummode,f,vs,vp,rho,thk,wave='rayleigh'):    
    velocity_model = np.vstack((np.atleast_2d(np.hstack((thk,0))),
                                np.atleast_2d(vp),
                                np.atleast_2d(vs),
                                np.atleast_2d(rho)))
    velocity_model = velocity_model/1000
    t = np.sort(np.squeeze(1/f))
    nf = len(np.squeeze(f))
    dc = np.zeros((nf,nummode))
    try:        
        pd = PhaseDispersion(*velocity_model,dc=0.005)
        for ii in range(nummode):
            cpr = pd(t,mode=ii,wave=wave).velocity
            dc[nf-len(cpr):,ii] = cpr[::-1]*1000  
    except:
         dc[:] = np.nan
    return dc

# def dc_fast_par(nummode,f,vs,vp,rho,thk,ncurv,wave='rayleigh'):
#     dc_mp=[]
#     for i in range(ncurv):
#         try:
#             dc_mp.append(dc_fast(nummode,f,vs[i],vp[i],rho[i],thk[i],wave=wave))
#         except:
#             print(i,vs[i],vp[i],rho[i],thk[i])        
#     return np.array(dc_mp)