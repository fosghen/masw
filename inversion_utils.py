import numpy as np
from disba import PhaseDispersion
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from multiprocessing import cpu_count
import pickle

def get_mean_mode0(dict_curv):
    sources = list(dict_curv.keys())
    modes = list(dict_curv[sources[0]].keys())

    fmin_mode0 = min([dict_curv[ii][modes[0]]["f"][0] for ii in sources])
    fmax_mode0 = max([dict_curv[ii][modes[0]]["f"][-1] for ii in sources])
    freq_mode0 = np.arange(fmin_mode0, fmax_mode0, 0.2)

    all_modes0 = np.array([interp1d(dict_curv[ii][0]['f'],
                                    dict_curv[ii][0]['V'],
                                    kind='nearest',
                                    fill_value='extrapolate')(freq_mode0)
                           for ii in dict_curv.keys()])
    mean_mode0 = np.mean(all_modes0, axis=0)

    return mean_mode0, freq_mode0, sources

def get_new_format_dc(dict_curv, sources, num_use_modes):

    fmin = min([dict_curv[ii][0]["f"][0] for ii in sources])
    fmax = max([dict_curv[ii][num_use_modes-1]["f"][-1] for ii in sources])
    freq = np.arange(fmin, fmax, 0.5)

    nf = len(freq)
    nsou = len(sources)

    all_new_dc = np.zeros((nf*num_use_modes, nsou))

    for ii in range(nsou):
        new_dc = []
        for jj in range(num_use_modes):
            new_dc.extend(interp1d(dict_curv[sources[ii]][jj]['f'],
                                   dict_curv[sources[ii]][jj]['V'],
                                   kind='linear',
                                   bounds_error=False,
                                   fill_value=(0, 0))(freq))
        all_new_dc[:, ii] = np.array(new_dc)

    return all_new_dc, freq, nf, nsou

def get_dict_curve(path):
    b_file = open(path, "rb")
    dict_curv = pickle.load(b_file)
    b_file.close()
    sources = list(dict_curv.keys())
    modes = list(dict_curv[sources[0]].keys())
    dx = dict_curv[sources[-1]][modes[-1]]['dx']
    L = dict_curv[sources[-1]][modes[-1]]['L']
    cmp = np.array(sources) + dx + L

    return dict_curv, sources, cmp


def mean_squared_error(y_true, y_pred, axis=(0, 1)):
    return np.mean(np.abs((y_true - y_pred) ** 2), axis)

def monte_carlo(dc_obs, dc_train, vs_train, thk_train):
    dc_obs_rep = np.squeeze(dc_obs)[None, ...].repeat(np.size(dc_train, 0), axis=0)
    ind = np.argmin(mean_squared_error(dc_obs_rep, dc_train, axis=1))
    vs_rest = vs_train[np.int32(ind), :]
    thk_rest = thk_train[np.int32(ind), :]
    dc_rest = dc_train[np.int32(ind)]
    return vs_rest, thk_rest, dc_rest


def dc_fast_par(nummode, f, vs, vp, rho, thk, ncurv, wave='rayleigh'):
    dc_mp = Parallel(n_jobs=cpu_count())(
        delayed(dc_fast_for_par)(nummode, f, vs[i], vp[i], rho[i], thk[i], wave=wave) for i in range(ncurv))
    return np.array(dc_mp)


def dc_fast_for_par(nummode, f, vs, vp, rho, thk, wave='rayleigh'):
    velocity_model = np.vstack((np.atleast_2d(np.hstack((thk, 0))),
                                np.atleast_2d(vp),
                                np.atleast_2d(vs),
                                np.atleast_2d(rho)))
    velocity_model = velocity_model / 1000
    t = np.sort(np.squeeze(1 / f))
    nf = len(np.squeeze(f))
    dc = np.zeros((nf, nummode))
    try:
        pd = PhaseDispersion(*velocity_model, dc=0.005)
        for ii in range(nummode):
            cpr = pd(t, mode=ii, wave=wave).velocity
            dc[nf - len(cpr):, ii] = cpr[::-1] * 1000
    except:
        dc[:] = np.nan
    return dc


def gettraindata(mrange, freq, nummode, ncurv=10, vs2vp=2, wave='rayleigh'):
    nlay = len(np.squeeze(mrange['vs_up']))
    vs_train = np.zeros((ncurv, nlay))
    thk_train = np.zeros((ncurv, nlay - 1))

    for i in range(nlay):
        vs_train[:, i] = np.random.randint(mrange['vs_up'][i] - mrange['vs_down'][i], size=ncurv) + mrange['vs_down'][i]
    for i in range(nlay - 1):
        thk_train[:, i] = np.round(
            (mrange['thk_up'][i] - mrange['thk_down'][i]) * np.random.rand(ncurv) + mrange['thk_down'][i], 1)

    vs_train = np.int32(vs_train)
    vp = np.int32(vs_train * vs2vp)
    rho = np.int32(0.61 * vp ** 0.18 * 1000)

    dc_train = dc_fast_par(nummode, freq, vs_train, vp, rho, thk_train, ncurv, wave=wave)

    ind_row_nan = np.unique(np.where(np.isnan(dc_train) == True)[0])
    dc_train_clear = np.delete(dc_train, ind_row_nan, axis=0)
    vs_train_clear = np.delete(vs_train, ind_row_nan, axis=0)
    thk_train_clear = np.delete(thk_train, ind_row_nan, axis=0)

    dc_train_all_sec_modes = []
    for ii in range(nummode):
        dc_train_all_sec_modes.extend(list(np.squeeze(dc_train_clear[:, :, ii].T)))
    dc_train_all_sec_modes = np.array(dc_train_all_sec_modes).T

    return dc_train_all_sec_modes, vs_train_clear, thk_train_clear


def thk1d2dep(thk, maxdep=0):
    thk = np.squeeze(thk)
    if np.size(thk) > 1:
        if thk[-1] == 0:
            thk = np.delete(thk, -1, -1)
    mindep = 0
    sum_thk = np.cumsum(thk)
    if maxdep < max(sum_thk) + 5:
        maxdep = max(sum_thk) + 5
    return np.hstack((mindep, sum_thk, maxdep))


def vs1d2vsplt(vs):
    vs = np.squeeze(vs)
    return np.hstack((vs, vs[-1]))


def dc_fast(nummode, f, vs, vp, rho, thk, wave='rayleigh'):
    velocity_model = np.vstack((np.atleast_2d(np.hstack((np.squeeze(thk), 0))),
                                np.atleast_2d(vp),
                                np.atleast_2d(vs),
                                np.atleast_2d(rho)))
    velocity_model = velocity_model / 1000
    t = np.sort(np.squeeze(1 / f))
    nf = len(np.squeeze(f))
    dc = np.zeros((nf, nummode))
    pd = PhaseDispersion(*velocity_model, dc=0.00005)
    for ii in range(nummode):
        cpr = pd(t, mode=ii, wave=wave).velocity
        dc[nf - len(cpr):, ii] = cpr[::-1] * 1000
    return dc


def getranges(dc, freq, xi, nummode, vs2vp, wave, dvs):
    dc = np.squeeze(dc)
    lc = dc / freq
    lmin = np.min(lc)
    d_res = np.max(lc) / 2

    d_min = []
    d_max = []
    i = 0
    d_temp = 0
    while d_temp < d_res:
        if i == 0:
            d_min.append(lmin / 3)
            d_max.append(lmin)
        elif i == 1:
            d_min.append(d_max[i - 1])
            d_max.append(d_min[i] + xi * lmin)
        else:
            d_min.append(d_max[i - 1])
            d_max.append(d_min[i] + xi * (d_max[i - 1] - d_min[i - 1]))
        d_temp = d_max[-1]
        i += 1

    if d_max[-1] > d_res:
        del d_max[-1]
        del d_min[-1]

    d_max = np.round(d_max, 1)
    d_min = np.round(d_min, 1)
    d_range = np.vstack(([d_min], [d_max]))

    thk_up = d_max - d_min
    thk_up[0] = d_max[0]
    thk_down = np.zeros(len(thk_up)) + np.round(lmin / 3, 1)

    lc = (dc / freq) * 0.53
    vr2vs = 1.16
    dep_mean = np.mean(d_range, 0)

    vs_mean = []
    for i in range(len(dep_mean)):
        vs_mean.append(vr2vs * dc[np.argmin(abs(lc - dep_mean[i]))])
    vs_mean.append(vr2vs * dc[0])
    vs_mean = np.int32(np.array(vs_mean))

    vs_up = vs_mean + dvs
    vs_down = vs_mean - dvs

    vs_diff = 50
    if np.where(vs_down < vs_diff)[0].size > 0:
        vs_down[np.where(vs_down < vs_diff)[0]] = vs_diff

    for i in range(1, len(vs_down)):
        if vs_down[i] - vs_down[i - 1] < vs_diff:
            vs_down[i] = vs_down[i - 1] + vs_diff

    for i in range(len(vs_down)):
        if vs_up[i] <= vs_down[i]:
            vs_up[i] = vs_down[i] + vs_diff

    #     if del1stlay:
    #         thk_up = np.delete(thk_up,0,-1)
    #         thk_down = np.delete(thk_down,0,-1)
    #         vs_up = np.delete(vs_up,0,-1)
    #         vs_down = np.delete(vs_down,0,-1)

    vp_down = np.int32(vs_down * vs2vp)
    vp_up = np.int32(vs_up * vs2vp)

    rho_down = np.int32(0.61 * vp_down ** 0.18 * 1000)
    rho_up = np.int32(0.61 * vp_up ** 0.18 * 1000)
    freq = np.atleast_2d(freq)
    dc_down = dc_fast(nummode, freq, vs_down, vp_down, rho_down, thk_up, wave=wave)
    dc_up = dc_fast(nummode, freq, vs_up, vp_up, rho_up, thk_down, wave=wave)

    range_model = {'vs_down': np.int32(vs_down),
                   'vs_up': np.int32(vs_up),
                   'thk_down': thk_down,
                   'thk_up': thk_up,
                   'vp_down': vp_down,
                   'vp_up': vp_up,
                   'rho_down': rho_down,
                   'rho_up': rho_up,
                   'dc_down': dc_down,
                   'dc_up': dc_up,
                   'd_range': d_range,
                   'freq': freq}

    return range_model


def get2dmodel(vs_rest, thk_rest, cmp, dy=0.1, cmp_new_n=2000):
    vs = np.array(vs_rest)
    thk = np.round(np.array(thk_rest), 1)
    nsou, nlay = np.shape(vs)
    max_dep = np.max(np.cumsum(thk,axis=1)) + 5

    ### подготовка толщин на новую сетку по y с шагом dy и перевод толщин в глубины
    thk_n = np.int32(thk / dy)
    dep_n = np.cumsum(thk_n, axis=1)

    ### Новый вектор cmp
    print(cmp)
    cmp_new = np.linspace(min(cmp), max(cmp), num=cmp_new_n, endpoint=True)

    if len(cmp) > 3:
        kind = 'cubic'
    else:
        kind = 'linear'

    ### создание матрицы границ в точках (шаг между точками dy м)
    dep_new_n = np.zeros((cmp_new_n, nlay + 1), dtype=int)
    for i in range(1, nlay):
        dep_new_n[:, i] = interp1d(cmp, dep_n[:, i - 1], kind=kind)(cmp_new)
    dep_new_n[:, nlay] = max_dep / dy

    ### 1д интерполяция Vs по x (для уравнивания количества точек с количеством точек в матрице границ)
    vs2d0 = np.zeros((nlay, cmp_new_n))

    for i in range(nlay):
        vs2d0[i, :] = interp1d(cmp, vs[:, i], kind=kind)(cmp_new)

    ### Заполнить значения Vs между границами
    vs2d1 = np.zeros((int(max_dep / dy), cmp_new_n))
    for i in range(nlay):
        for j in range(cmp_new_n):
            vs2d1[dep_new_n[j, i]:dep_new_n[j, i + 1] + 1, j] = vs2d0[i, j]

    return vs2d1, dep_new_n, cmp_new, nlay


def draw2dmodel(ax, vs2d, dep2d, cmp2d, nlay, dy=0.1):
    vmin, vmax = np.min(vs2d), np.max(vs2d)
    im = ax.imshow(vs2d, aspect='auto', cmap='jet',
                   extent=[np.min(cmp2d), np.max(cmp2d), np.max(dep2d) * dy, np.min(dep2d) * dy],
                   vmin=vmin, vmax=vmax, interpolation='nearest')
    # for i in range(1, nlay):
    #     ax.plot(cmp2d, dep2d[:, i] * dy, '--k', lw=2)
    cbar = plt.colorbar(mappable=im, ax=ax, aspect=10, pad=0.01)
    ax.annotate(r'$V_S$ (м/с)', xy=(0, 0), xytext=(1, 1.05), xycoords='axes fraction', color='#bebebe')
    # ax.xaxis.set_tick_params(labelsize=20)
    # ax.yaxis.set_tick_params(labelsize=20)
    ax.set_ylabel('Depth (m)', color = '#bebebe')
    ax.set_xlabel('X (m)', labelpad=-0.05, color = '#bebebe')
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
    cbar.ax.yaxis.set_tick_params(color='#bebebe')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#bebebe')
    cbar.outline.set_edgecolor(color='#bebebe')

    return cbar


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


def get1dc(path):
    b_file = open(path, "rb")
    dict_curv = pickle.load(b_file)
    b_file.close()
    sou = list(dict_curv.keys())[0]

    freq0 = dict_curv[sou][0]['f']
    mode0 = dict_curv[sou][0]['V']
    return mode0



