import numpy as np
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from stock import stran

def freqloop(f_i,FTX,nt,nr,new_nr,incline):

    TX = np.squeeze(FTX[f_i,:,:])
    TX = TX/np.amax(abs(TX),axis=0)

    fk_vg = np.zeros((nt,new_nr),dtype=complex)
    line_phase = np.zeros((nr,nt),dtype=complex)    

    for i in range(nt): 
        for j in range(nr):
            line_phase[j,i] = TX[incline[j,i],j]
        fk_vg[i,0:nr] = line_phase[:,i]
    fk_vg2 = abs(np.fft.fft(fk_vg,axis=1))[:,::-1]
    fk2d_f_i = np.amax(fk_vg2,axis=0)
    
    return fk2d_f_i

def SFK(data,dt,dr,fmin=0,fmax=100,offset0=0,multi_nt=1,multi_nr=50,width=0.5):
    
    # data - seismogramm-matrix
    # dt - sample rate by time in seconds
    # dr - reciever step 
    # fmin, fmax - minimal and maximum frequencies in spectrum
    # multi_nt - multiplier to increase time dimension
    # multi_nr - multiplier to increase distance dimension
    # width - width Gaussin window from 0.1 to 1.
    
    nr = min(np.shape(data))
    nt = max(np.shape(data))
    new_nt = multi_nt*nt
    new_nr = multi_nr*nr
    df = 1/dt/new_nt
    dk = 1/dr/new_nr
    k = np.arange(0,new_nr*dk,dk)
    freq = np.arange(fmin,fmax,df)
#     fk2d = np.zeros((np.size(freq),np.size(k)))
    min_nf = int(fmin/df)
    max_nf = int(fmax/df)
    FTX = np.zeros((max_nf-min_nf,new_nt,nr),dtype=complex)
    FTX_old = FTX.copy()
    new_data = np.zeros((new_nt,nr))
    new_data[0:nt,:] = data

    it = np.arange(0,nt)[None,...]+offset0/dr
    ir = np.arange(0,nr)[None,...]/(nr+offset0/dr)
    incline = np.zeros((nr,nt),dtype=int)
    incline = np.minimum(it*ir.T,np.zeros(np.shape(incline))+nt).astype(int)
    
    for i in range(nr):
        FTX[:,:,i] = stran(new_data[:,i][None,None,...],1/dt,fmin=fmin,fmax=fmax,n_fft=new_nt,width=width)
    freqc = np.float32(freq[:len(FTX[:,0,0])])

    fk2d_list = Parallel(n_jobs=cpu_count())(delayed(freqloop)(f_i,FTX,nt,nr,new_nr,incline) for f_i in range(np.size(freqc)))
    fk2d = np.array(fk2d_list)

#    fk = np.argmax(fk2d,1)*dk
#    np.seterr(divide='ignore', invalid='ignore')
#    vf = freqc/fk

    # fk2d - spectr matrix
    # freqc - frequencies vector
    # k - wavenumber vector
    return fk2d, freqc, k


def fk2vf(fk2d,
          freq, k,
          maxVel=1000, multi_k = 50):

    new_k = np.arange(0, multi_k * np.size(fk2d, 1), 1) * (k[1] - k[0])
    new_k = np.array([new_k[1:]]).T
    freq = np.array([freq])
    vel = freq / new_k

    new_fk = np.tile(fk2d, multi_k)
    vf2d = np.zeros((maxVel, np.size(freq)))

    for i in range(np.size(freq)):
        vf2d[vel[np.where(vel[:, i] < maxVel), i].astype(int), i] = new_fk[i, np.where(vel[:, i] < maxVel)]

    for i in range(np.size(vf2d, 1)):
        for j in range(np.size(vf2d, 0)):
            if vf2d[j, i] == 0:
                vf2d[j, i] = vf2d[j - 1, i]

    return vf2d