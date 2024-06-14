# cliping: функция, обрезающая пики, которые больше единицы и делает их равными единице

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
from inversion_utils import vs1d2vsplt, thk1d2dep
from collections import Counter


def cliping(trace):
    trace[np.abs(trace) > 1] = 1
    return trace

# drow_seismogram: функция отрисовки сейсмограмм
# data - данные, матрица, nt - кол-во отсчётов времени
# dt - длина отсчёта, nx - шаг между источниками
# clip - клипинг. figsize - размер окна
# scale - усиление


def drow_seismogram(axis, data, nt, dt, nx, dr, offsets, clip = False, figsize = (16, 8), scale = 1):
    #fig, ax = plt.subplots(figsize = figsize)
    ax = axis
    for i in range(len(offsets)):
        trace = data[:, i]
        trace_norm = scale*trace/np.max(trace)
        if clip:
            trace_norm = cliping(trace_norm)

        tmp_offset = min(offsets) + dr*i
        x = trace_norm + tmp_offset
        time = np.arange(0, nt * dt, dt)[:len(x)]
        ax.plot(x, time, c = 'k')
        # ax.fill_betweenx(time, tmp_offset, x, where=(trace_norm>=0), color='k')
    
    ax.tick_params(axis = 'both',
               direction = 'out',
               pad = 10, 
               top = True,
               bottom = False,
               left = True, 
               labeltop = True,
               labelbottom = False,    
               labelleft = True,
               color = '#bebebe', colors='#bebebe')
    ax.spines[:].set_color('#bebebe')

    ax.set_xlabel("Offset, m", fontsize = 15, labelpad = 10, color = '#bebebe')
    ax.set_ylabel("Time, s", fontsize = 15, color = '#bebebe')
    ax.set_ylim([nt * dt,0])
    ax.set_xlim([min(offsets), max(offsets)])
    plt.xticks(offsets[::10])
 
def draw_spectr(ax, spectr, freq, vmax, vmin):
    ax.imshow(spectr, aspect='auto', extent=[min(freq),max(freq),vmin,vmax], cmap='viridis',origin = 'lower')
    ax.set_xlabel("Frequency, Hz", fontsize = 14, labelpad = -1, color = '#bebebe')
    ax.set_ylabel("Phase velocity, m/s", fontsize = 14, color = '#bebebe')
    ax.tick_params(axis='both',
                   direction='out',
                   top=False,
                   bottom=True,
                   left=True,
                   labeltop=False,
                   labelbottom=True,
                   labelleft=True,
                   color='#bebebe', colors='#bebebe')
    ax.spines[:].set_color('#bebebe')

def draw1dmodel(ax_vs, ax_dc, model_range, vs, thk, new_dc, dc_rest, freq, num_use_modes, fontsize):

    maxdep = max(np.cumsum(model_range['thk_up'])) + 5

    vs_down_limit = vs1d2vsplt(model_range['vs_down'])
    vs_up_limit = vs1d2vsplt(model_range['vs_up'])
    vs_rest = vs1d2vsplt(vs)
    depth_up_limit = thk1d2dep(model_range['thk_up'], maxdep=maxdep)
    depth_down_limit = thk1d2dep(model_range['thk_down'], maxdep=maxdep)
    dep_rest = thk1d2dep(thk, maxdep=maxdep)

    ax_vs.step(vs_rest, dep_rest, linestyle='-', color="k", lw=3, label='Restored')
    ax_vs.step(vs_down_limit, depth_up_limit, linestyle='--', color='darkblue', lw=2, label='Limits')
    ax_vs.step(vs_up_limit,depth_down_limit, linestyle='--', color='darkblue', lw=2)
    ax_vs.set_ylim([maxdep, 0])
    ax_vs.yaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax_vs.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax_vs.xaxis.set_tick_params(labelsize=fontsize)
    ax_vs.yaxis.set_tick_params(labelsize=fontsize)

    ax_vs.tick_params(axis='both',
                      direction='out',
                      top=False,
                      bottom=True,
                      left=True,
                      labeltop=False,
                      labelbottom=True,
                      labelleft=True)
    ax_vs.spines[:].set_color('k')
    ax_vs.set_xlabel(r'$V_S$ (m/s)', fontsize=fontsize)
    ax_vs.set_ylabel('Depth (m)', fontsize=fontsize)
    ax_vs.set_facecolor(color='#bebebe')
    legend = ax_vs.legend(loc='upper right', fontsize=fontsize)
    frame = legend.get_frame()
    frame.set_edgecolor('k')
    frame.set_facecolor('#bebebe')
    freq = np.squeeze(freq)
    nf = len(freq)
    new_dc = np.squeeze(new_dc)
    dc_rest = np.squeeze(dc_rest)
    new_dc[np.where(new_dc == 0)] = np.nan
    dc_rest[np.where(dc_rest == 0)] = np.nan

    ax_dc.plot(freq, new_dc[:nf], linestyle='-', c="darkred", lw=3, label="Experimental")
    ax_dc.plot(freq, dc_rest[:nf], linestyle='-', c="k", lw=3, label="Restored")

    for ii in range(1,num_use_modes):
        ax_dc.plot(freq, new_dc[nf*ii:nf*(ii+1)], linestyle='-', c="darkred", lw=3)
        ax_dc.plot(freq, dc_rest[nf*ii:nf*(ii+1)], linestyle='-', c="k", lw=3)

    # ax_dc.plot(np.squeeze(model_range['freq']),
    #            np.squeeze(model_range['dc_down']), linestyle='--', color='darkblue', lw=2)
    # ax_dc.plot(np.squeeze(model_range['freq']),
    #            np.squeeze(model_range['dc_up']), linestyle='--', color='darkblue', lw=2, label="Limits")
    ax_dc.set_xlim([np.min(freq), np.max(freq)])
    ax_dc.set_ylim([0, np.max(model_range['dc_up'])+100])
    ax_dc.tick_params(axis='both',
                      direction='out',
                      top=False,
                      bottom=True,
                      left=True,
                      labeltop=False,
                      labelbottom=True,
                      labelleft=True)
    ax_dc.spines[:].set_color('k')
    ax_dc.set_facecolor(color='#bebebe')
    ax_dc.yaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax_dc.xaxis.set_major_formatter(FormatStrFormatter('%g'))
    ax_dc.set_ylabel('Phase velocity (m/s)', fontsize=fontsize)
    ax_dc.set_xlabel('Frequency (Hz)', fontsize=fontsize)
    ax_dc.xaxis.set_tick_params(labelsize=fontsize)
    ax_dc.yaxis.set_tick_params(labelsize=fontsize)
    legend = ax_dc.legend(loc='upper right', fontsize=fontsize)
    frame = legend.get_frame()
    frame.set_edgecolor('k')
    frame.set_facecolor('#bebebe')


