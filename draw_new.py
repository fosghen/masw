# cliping: функция, обрезающая пики, которые больше единицы и делает их равными единице

import matplotlib.pyplot as plt
import numpy as np

def draw_spectr_outside(spectr, freq, vmax):
    # fig, ax = plt.subplots(1,1)
    ax.imshow(spectr**2, aspect='auto', extent=[min(freq),max(freq),0,vmax], cmap='viridis',origin = 'lower')
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
    # plt.show()
