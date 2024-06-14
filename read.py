import os
import segyio
import numpy as np


# get_names: получение имён файлов в директории path

def get_names(path):
    return os.listdir(path)


# read_segy_file: чтение segy файла в директории path

def read_segy_file(path):
    try:
        segy_file = segyio.open(path, ignore_geometry='True', endian='big')
    except:
        segy_file = segyio.open(path, ignore_geometry='True', endian='little')
    return segy_file


# get_all_attributes: получение всех необходимых атрибутов из segy файла

def get_all_attributes(segy_file):
    group_x = segy_file.attributes(segyio.TraceField.GroupX)[:]
    sou_x = segy_file.attributes(segyio.TraceField.SourceX)[0]
    dt = segyio.dt(segy_file)*1e-6
    dx = abs(group_x[1] - group_x[0])
    data = np.array([np.copy(tr) for tr in segy_file.trace[:]]).T
    nt, nx = np.shape(data)
    attributes = {"data": data, "nt": nt, "dt": dt, "nx": nx, "dx" : dx, "rec_x": group_x, "sou_x": sou_x}
    return attributes

def get_sources(path):
    srs = get_all_attributes(read_segy_file(path))
    sourses = float(srs["sou_x"])
    del srs["sou_x"]
    return sourses, srs