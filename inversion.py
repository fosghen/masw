from inversion_utils import *
from search_xi import *
from GWO_mp import GWOmp
import copy

def inversion_run(dict_curv, optimizer, num_use_modes):

    all_xi = [1.3, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    vs2vp = 2
    dvs = 300
    wave = 'rayleigh'
    max_iter_gwo = 50
    ncurv_mc = 30000

    mean_mode0, freq_mode0, sources = get_mean_mode0(dict_curv) # осреднить нулевую моду по все источникам
    vs_rest_xi, thk_rest_xi, dc_rest_xi = search_xi(mean_mode0, freq_mode0, all_xi, vs2vp, dvs, wave, ncurv=10, num_search=1)  #расчет моделей и кривых для разной параметризации
    # xi = get_xi(mean_mode0, dc_rest_xi) #поиск оптимальной параметризации
    xi = 3.5
    model_range = getranges(mean_mode0, freq_mode0, xi, 1, vs2vp, wave, dvs) #рассчитать диапазоны для модели с оптимальной параметризацией
    nlay = np.size(model_range['vs_down'])
    print('Optimal Xi = ' + str(xi) + ' (' + str(nlay) + ' layers)')

    new_dc, freq, nf, nsou = get_new_format_dc(dict_curv, sources, num_use_modes) #подготовка данных в новый формат - матрица размерами (nf*num_use_mode)Xnsou

    vs_rest = np.zeros((nsou, nlay))
    thk_rest = np.zeros((nsou, nlay-1))
    dc_rest = np.zeros((nsou, nf*num_use_modes))

    if optimizer == "mc":
        dc_train, vs_train, thk_train = gettraindata(model_range, freq, num_use_modes, vs2vp=vs2vp, wave=wave, ncurv=ncurv_mc)
        for ii in range(nsou):
            dc_train_ii = copy.deepcopy(dc_train)
            dc_train_ii[:, np.where(new_dc[:, ii] == 0)[0]] = 0
            vs_rest[ii, :], thk_rest[ii, :], dc_rest[ii, :] = monte_carlo(new_dc[:, ii], dc_train_ii, vs_train, thk_train)

    if optimizer == "gwo":
        for ii in range(nsou):
            vs_rest[ii, :], thk_rest[ii, :] = GWOmp(new_dc[:, ii], freq, num_use_modes, model_range, vs2vp, wave, max_iter_gwo)
            vp = np.int32(vs_rest[ii, :]*vs2vp)
            rho = np.int32(0.61*np.int32(vs_rest[ii, :]*vs2vp)**0.18*1000)
            dc_rest[ii, :] = dc_fast(num_use_modes, freq, vs_rest[ii, :], vp, rho, thk_rest[ii, :], wave=wave).T.flatten()
            dc_rest[ii, np.where(new_dc[:, ii] == 0)[0]] = 0

    return vs_rest, thk_rest, dc_rest, freq, new_dc, mean_mode0, freq_mode0, all_xi, xi, vs_rest_xi, thk_rest_xi, dc_rest_xi, model_range