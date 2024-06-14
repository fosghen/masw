import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from inversion_utils import getranges
from get_train_data import gettraindata
from monte_carlo import monte_carlo as mc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
matplotlib.use('qt5agg')



class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

def thk1d2dep(thk,maxdep=0):
    
    thk = np.squeeze(np.array(thk))
    if np.size(thk)>1:
        if thk[-1] == 0:
            thk = np.delete(thk,-1,-1)
    mindep = 0
    sum_thk = np.cumsum(thk)
    if maxdep < max(sum_thk)+5:
        maxdep = max(sum_thk)+5    
        
    return np.hstack((mindep,sum_thk,maxdep))

def vs1d2vsplt(vs):
    
    vs = np.squeeze(np.array(vs))
    return np.hstack((vs,vs[-1]))
    
def search_xi(dc, freq, all_xi, vs2vp, dvs, wave, ncurv=100,num_search=10):

    nummode = 1
    dc = np.atleast_2d(dc)
    freq = np.atleast_2d(freq)    
    dc_rest_xi,vs_rest_xi,thk_rest_xi = {},{},{}    
    
    for xi in all_xi:
        print('Xi = ', xi)        
        dc_rest,vs_rest,thk_rest = [],[],[]        
        
        for ii in range(num_search):            
            model_range = getranges(dc, freq, xi, nummode, vs2vp, wave, dvs)
            dc_train, vs_train, thk_train = gettraindata(model_range, freq, nummode, ncurv=ncurv, vs2vp=vs2vp, wave=wave)
            ind = mc(dc,dc_train)
            dc_rest.append(np.squeeze(dc_train[np.int32(ind),:]))
            vs_rest.append(np.squeeze(vs_train[np.int32(ind),:]))
            thk_rest.append(np.squeeze(thk_train[np.int32(ind),:]))
            
        dc_rest_xi[xi] = np.array(dc_rest)
        vs_rest_xi[xi] = np.array(vs_rest)
        thk_rest_xi[xi] = np.array(thk_rest)

    return vs_rest_xi,thk_rest_xi,dc_rest_xi

def get_xi(dc_true,dc_rest_xi,fontsize=16,fs=(8,4)):
    
    cmse,med_cmse = [],[]
    dc_true = np.atleast_2d(np.squeeze(dc_true))
    all_xi = list(dc_rest_xi.keys())
    for xi in all_xi:
        dc_rest_full = np.atleast_2d(dc_rest_xi[xi])
        ns = np.size(dc_rest_full,0)
        dc_true_full = np.repeat(dc_true,ns,axis=0)
        cmse1 = np.mean((dc_true_full - dc_rest_full)**2,axis=1)
        med_cmse.append(np.median(cmse1))
        cmse.extend(cmse1)
    xi_opt = all_xi[np.argmin(med_cmse)]
    
    #axs = figure.axes
    
    #axs.plot(np.repeat(all_xi,ns),cmse,'.k',ms=15)
    #axs.plot(all_xi,med_cmse,'.-b',ms=15)
    #axs.plot(xi,med_cmse[np.argmin(med_cmse)],'*r',ms=15)
    #axs.xaxis.set_tick_params(labelsize=fontsize)
    #axs.yaxis.set_tick_params(labelsize=fontsize)
    #axs.set_ylabel(r'$V_R^{MSE}$',fontsize=fontsize)
    #axs.set_xlabel(r'Layering ratio $(\Xi)$',fontsize=fontsize)
    #axs.set_yscale('log')
    #axs.grid()
    #figure.draw()
    
    return xi_opt

def plot_model_vs_xi(num_xi, ax1, ax2, figure, vs_rest_xi, thk_rest_xi, dc_rest_xi, freq_mode0, dc_true, vs2vp, dvs, wave, fontsize):

    nummode = 1
    all_xi = list(vs_rest_xi.keys())
    dc_true = np.atleast_2d(np.squeeze(dc_true))
    freq = np.squeeze(freq_mode0)
    xi = all_xi[num_xi]
    model_range = getranges(dc_true, freq, xi, nummode, vs2vp, wave, dvs)
    var = Bunch(model_range)
    maxdep = max(np.cumsum(var.thk_up)) + 5
    dep_down = thk1d2dep(var.thk_down,maxdep=maxdep)
    dep_up = thk1d2dep(var.thk_up,maxdep=maxdep)
    vs_down_plt = vs1d2vsplt(var.vs_down)
    vs_up_plt = vs1d2vsplt(var.vs_up)
    ax2.plot(freq, np.squeeze(dc_true), linestyle='-', color='darkred', lw=3, label="Experimental")

    ns = np.size(vs_rest_xi[xi], 0)
    for jj in range(ns-1):
        vs_rest_plt = vs1d2vsplt(vs_rest_xi[xi][jj,:])
        dep_rest = thk1d2dep(thk_rest_xi[xi][jj,:],maxdep=maxdep)
        ax1.step(vs_rest_plt,dep_rest,linestyle='--',color='k',lw=2)

    vs_rest_plt = vs1d2vsplt(vs_rest_xi[xi][-1, :])
    dep_rest = thk1d2dep(thk_rest_xi[xi][-1, :], maxdep=maxdep)
    ax1.step(vs_rest_plt, dep_rest, linestyle='--', color='k', lw=2, label="Restored")
    if np.size(dc_rest_xi[xi], 0) > 1:
        ax2.plot(freq, np.squeeze(dc_rest_xi[xi])[:-1,:].T, linestyle='--', color='k', lw=2)
        ax2.plot(freq, np.squeeze(dc_rest_xi[xi])[-1,:], linestyle='--', color='k', lw=2, label="Restored")
    else:
        ax2.plot(freq, np.squeeze(dc_rest_xi[xi]), linestyle='--', color='k', lw=2, label="Restored")
        
    #if len(true_model):
     #   vs_true_plt = vs1d2vsplt(true_model[0])
     #   dep_true = thk1d2dep(true_model[1],maxdep=maxdep)
      #  axs[ii,0].step(vs_true_plt,dep_true,'r',lw=2)

    ax1.step(vs_down_plt,dep_up,linestyle='--',color='darkblue',lw=2,label="Limits")
    ax1.step(vs_up_plt,dep_down,linestyle='--',color='darkblue',lw=2)
    ax2.plot(freq,np.squeeze(var.dc_down),linestyle='--',color='darkblue',lw=2,label="Limits")
    ax2.plot(freq,np.squeeze(var.dc_up),linestyle='--',color='darkblue',lw=2)

    ax1.set_ylim([maxdep,0])
    ax1.set_xlabel(r'$V_S$ (m/s)', fontsize=fontsize)
    ax1.set_ylabel('Depth (m)', fontsize=fontsize)
    # ax1.set_title(str(len(np.squeeze(var.vs_down))) + ' layers', fontsize=fontsize)
    ax1.set_facecolor(color='#bebebe')
    ax1.xaxis.set_tick_params(labelsize=fontsize)
    ax1.yaxis.set_tick_params(labelsize=fontsize)

    # ax2.set_title(r'$\Xi$ = ' + str(xi) + ' (' + str(len(np.squeeze(var.vs_down))) + ' layers)', fontsize=fontsize)
    ax2.set_xlim([np.min(freq),np.max(freq)])
    ax2.set_ylim([0, np.max(var.dc_up)+100])
    ax2.set_xlabel(r'$f$ (1/s)', fontsize=fontsize)
    ax2.set_ylabel(r'$V_R$ (m/s)', fontsize=fontsize)
    ax2.xaxis.set_tick_params(labelsize=fontsize)
    ax2.yaxis.set_tick_params(labelsize=fontsize)
    ax2.set_facecolor(color='#bebebe')
    legend = ax1.legend(loc='upper right', fontsize=fontsize)
    frame = legend.get_frame()
    frame.set_edgecolor('k')
    frame.set_facecolor('#bebebe')
    legend = ax2.legend(loc='upper right', fontsize=fontsize)
    frame = legend.get_frame()
    frame.set_edgecolor('k')
    frame.set_facecolor('#bebebe')
    #figure.draw()