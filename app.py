# self.label_ed.setText(str(self.keys_data[self.count - 1]))

import os
import sys
import numpy as np
import segyio
from pathlib import Path
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import *
from read import *
from draw import *
from search_xi import *
import design
import plot_dc
import plot_xi
from sfk import SFK, fk2vf
from seiswindow import seiswindow
from inversion_utils import *
from inversion import inversion_run, get_dict_curve
import read as rfiles
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
import pickle
import matplotlib
import PySide2
from PySide2.QtGui import QMovie, QPixmap, QPainter
from PySide2.QtCore import QSize
matplotlib.rcParams["toolbar"] = 'None'
import time
import copy
from mplwidget import MplWidget
from matplotlib.ticker import FormatStrFormatter


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()  # QtCore.Slot
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class Plot_DC(QWidget, plot_dc.Ui_Plot_DC):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(865, 600)
        self.setWindowTitle(QCoreApplication.translate("WavesStrider", u"WavesStrider", None))
        icon = QIcon()
        icon.addFile(u":/icons/iconofwind.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setStyleSheet(u"QWidget {\n"
"	\n"
"	background-color: rgb(60, 63, 65);\n"
"}")

        

class Plot_XI(QWidget, plot_xi.Ui_Plot_XI):
    """
    This "window" is a QWidget. If it has no parent,
    it will appear as a free-floating window.
    """

    def __init__(self):        
        super().__init__()
        self.setupUi(self)
        self.resize(1200, 600)
        self.setWindowTitle(QCoreApplication.translate("WavesStrider", u"WavesStrider", None))
        icon = QIcon()
        icon.addFile(u":/icons/iconofwind.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.setStyleSheet(u"QWidget {\n"
"	\n"
"	background-color: rgb(60, 63, 65);\n"
"}")



class App(QMainWindow, design.Ui_WavesStrider):


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Open_File.clicked.connect(self.file_open)
        self.cliping_box.stateChanged.connect(self.change_clip)
        self.gane_spin.valueChanged.connect(self.change_gane)
        self.button_compute_in_spectr.clicked.connect(self.threads_of_compute_spectr)
        self.button_next_in_seis.clicked.connect(self.next_data)
        self.button_back_in_seis.clicked.connect(self.last_data)
        self.button_cut.clicked.connect(self.cut)
        self.pushButton.clicked.connect(self.threads_of_compute_model)
        self.cumpute_gwo.clicked.connect(self.threads_of_compute_model_gwo)
        self.spinBox.valueChanged.connect(self.change_mod)
        self.delete_mode_in_spectr.clicked.connect(self.delete_mode)
        self.button_save_in_spectr.clicked.connect(self.save)

        self.seismograms_widget.setVisible(False)
        self.button_next_in_spectr.clicked.connect(self.next_spectr)
        self.button_last_in_spectr.clicked.connect(self.prev_spectr)


        ## DEFAULT PARAMETERS


        ### seism parameters:
        self.dict_data = {}
        self.gane = 1
        self.sou = 0
        self.dr = 0
        self.nx = 0

        ### spectral parameters:
        self.dict_spectr = {}
        self.xs = []
        self.ys = []
        self.keys_data = []
        self.dict_data_cut = {}
        self.spectr_count = -1
        self.dv = 1
        self.df = 1
        self.width = 50
        self.vf2d = 0
        self.mod = 0
        self.sou_desp = 0
        self.fmin = 0
        self.fmax = 30
        self.minVel = 0
        self.maxVel = 500

        ### inversion parameters:
        self.all_data = {}
        self.xi = None
        self.sou_dc_gwo = 0
        self.vs2vp = 2
        self.dvs = 300
        self.wave = 'rayleigh'
        self.dc_count = 1
        self.dc_count_gwo = 1
        self.xi_count = 1
        self.xi_count_gwo = 1
        self.count = -1
        self.num_use_modes = 3

        ### addition parameters:
        self.curves = {}
        self.dictmod = {}
        self.fontsize = 16
        self.tmp_path = 'tmp/'
        self.curves_path = self.tmp_path + 'curves.pkl'
        self.cbar = None
        self.sc_mc = None
        self.threadpool = QThreadPool()
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.is_xi_comp = False
        self.optimizer = ''
        self.counter = 0
        self.clip = False




        # print("Multithreading with maximum %d threads" % self.threadpool.activeThreadCount())
        self.TAB.setEnabled(True)
        self.cliping_box.setEnabled(True)
        self.gane_spin.setEnabled(True)
        self.label_gane.setEnabled(True)
        self.label_receiver.setEnabled(True)
        self.label_masw.setEnabled(True)
        self.edit_receiver.setEnabled(True)
        self.edit_masw.setEnabled(True)
        self.button_cut.setEnabled(True)
        
        self.plot_xi = Plot_XI()
        self.plot_dc = Plot_DC()
        self.plot_dc.setVisible(False)
        self.plot_xi.setWindowTitle(QCoreApplication.translate("XI Monte-Carlo", u"XI Monte-Carlo", None))
        self.plot_dc.setWindowTitle(QCoreApplication.translate("DC Monte-Carlo", u"DC Monte-Carlo", None))
        
        self.plot_xi_gwo = Plot_XI()
        self.plot_dc_gwo = Plot_DC()
        self.plot_xi_gwo.setWindowTitle(QCoreApplication.translate("XI GWO", u"XI GWO", None))
        self.plot_dc_gwo.setWindowTitle(QCoreApplication.translate("DC GWO", u"DC GWO", None))
        
        
        self.plot_dc.button_next_in_dc.clicked.connect(self.next_dc)
        self.plot_dc.button_back_in_dc.clicked.connect(self.prev_dc)
        
        self.plot_xi.button_next_in_xi.clicked.connect(self.next_xi)
        self.plot_xi.button_back_in_xi.clicked.connect(self.prev_xi)
        
        
        self.plot_dc_gwo.button_next_in_dc.clicked.connect(self.next_dc_gwo)
        self.plot_dc_gwo.button_back_in_dc.clicked.connect(self.prev_dc_gwo)
        
        self.plot_xi_gwo.button_next_in_xi.clicked.connect(self.next_xi_gwo)
        self.plot_xi_gwo.button_back_in_xi.clicked.connect(self.prev_xi_gwo)
        
        self.toolbar1 = NavigationToolbar(self.seismograms_widget.canvas, self)
        #self.toolbar1.setStyleSheet("background-color:Gray;")

        unwanted_buttons = ['Back', 'Forward', 'Subplots', 'Customize']
        for x in self.toolbar1.actions():
            if x.text() in unwanted_buttons:
                self.toolbar1.removeAction(x)


        self.verticalLayout_4.addWidget(self.toolbar1)
        self.toolbar2 = NavigationToolbar(self.dispersion.canvas, self)
        for x in self.toolbar2.actions():
            if x.text() in unwanted_buttons:
                self.toolbar2.removeAction(x)
        self.verticalLayout_2.addWidget(self.toolbar2)
        self.toolbar3 = NavigationToolbar(self.model_gwo.canvas, self)
        self.toolbar4 = NavigationToolbar(self.model.canvas, self)
        for x in self.toolbar3.actions():
            if x.text() in unwanted_buttons:
                self.toolbar3.removeAction(x)
        self.verticalLayout_5.addWidget(self.toolbar3)
        
        for x in self.toolbar4.actions():
            if x.text() in unwanted_buttons:
                self.toolbar4.removeAction(x)
        self.verticalLayout_7.addWidget(self.toolbar4)
        
        self.dispersion.setVisible(False)
        self.model.setVisible(False)
        self.model_gwo.setVisible(False)
        self.toolbar1.setVisible(False)
        self.toolbar2.setVisible(False)
        self.toolbar3.setVisible(False)
        self.toolbar4.setVisible(False)
        self.progressBar.setVisible(False)
        self.progressBar_2.setVisible(False)

        self.dispersion.canvas.mpl_connect('button_press_event', self.mouse_press)





    def next_dc(self):
        if -1 < self.dc_count < len(self.keys_data):
            self.dc_count += 1
            self.sou_dc = self.keys_data[self.dc_count - 1]
            self.plot_dc.label_coord_in_seis.setText(str(self.sou_dc))
            self.draw_dc()
   

    def prev_dc(self):
        if self.dc_count > 1:
            self.dc_count -= 1
            self.sou_dc = self.keys_data[self.dc_count - 1]
            self.plot_dc.label_coord_in_seis.setText(str(self.sou_dc))
            self.draw_dc()
    

    def next_xi(self):
        if -1 < self.xi_count < len(self.all_xi):
            self.xi_count += 1
            self.draw_xi()
 
 
    def prev_xi(self):
        if self.xi_count > 1:
            self.xi_count -= 1
            self.draw_xi()
    

    def next_dc_gwo(self):
        if -1 < self.dc_count_gwo < len(self.keys_data):
            self.dc_count_gwo += 1
            self.sou_dc_gwo = self.keys_data[self.dc_count_gwo - 1]
            self.plot_dc_gwo.label_coord_in_seis.setText(str(self.sou_dc_gwo))
            self.draw_dc_gwo()
   

    def prev_dc_gwo(self):
        if self.dc_count_gwo > 1:
            self.dc_count_gwo -= 1
            self.sou_dc_gwo = self.keys_data[self.dc_count_gwo - 1]
            self.plot_dc_gwo.label_coord_in_seis.setText(str(self.sou_dc_gwo))
            self.draw_dc_gwo()


    def next_xi_gwo(self):
        if -1 < self.xi_count_gwo < len(self.all_xi):
            self.xi_count_gwo += 1
            self.draw_xi_gwo()
    
 
    def prev_xi_gwo(self):
        if self.xi_count_gwo > 1:
            self.xi_count_gwo -= 1
            self.draw_xi_gwo()
    

    def file_open(self):
        self.paths, _ = QFileDialog.getOpenFileNames(self, "Choose seismogram files", "", "files (*.segy *.sgy)")
        if len(self.paths) == 0:
            return
        self.progressBar.setVisible(False)
        self.progressBar_2.setVisible(False)
        self.dispersion.setVisible(False)
        self.toolbar2.hide()
        self.seismograms_widget.hide()
        self.verticalSpacer_2.changeSize(20, 99999999)
        self.count = -1
        self.spectr_count = -1
        self.keys_spectr = {}
        self.sou_desp = {}
        self.vf2d = {}
        self.dictmod = {}
        self.curves = {}
        self.counter = 0


        self.dx = 1
        self.dict_data = {}
        self.dict_spectr = {}
        self.count = -1
        self.all_data = {}
        self.sou = 0
        self.dr = 0
        self.nx = 0
        self.xs = []
        self.ys = []
        self.dict_data_cut = {}

        self.count = 1
        for i in self.paths:
            key, data = rfiles.get_sources(i)
            self.dict_data[key] = data

        self.dict_data_orig = copy.deepcopy(self.dict_data)

        self.TAB.setEnabled(True)
        self.seismograms_widget.setVisible(True)
        self.verticalSpacer.changeSize(20, 0)
        self.keys_data = list(self.dict_data.keys())
        self.sou = self.keys_data[0]
        self.dr = self.dict_data[self.sou]["dx"]
        self.nx = self.dict_data[self.sou]["nx"]
        self.update_graph()
        # self.draw(self.dict_data[self.keys_data[0]])
        self.label_coord_in_seis.setText(str(self.sou))
        self.button_compute_in_spectr.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.toolbar1.setVisible(True)
    

    def draw(self, all_data):
        drow_seismogram(self.seismograms_widget.canvas.axes, all_data["data"], all_data["nt"],
                        all_data["dt"], all_data["nx"], all_data["dx"], scale=self.gane,
                        offsets=all_data["rec_x"], clip=self.clip)
        self.seismograms_widget.canvas.draw()


    def last_data(self):
        if self.count > 1:
            self.count -= 1
            self.update_graph()
            self.sou = self.keys_data[self.count - 1]
            self.label_coord_in_seis.setText(str(self.sou))
            self.dr = self.dict_data[self.sou]['dx']


    def next_data(self):
        if -1 < self.count < len(self.keys_data):
            self.count += 1
            self.update_graph()
            self.sou = self.keys_data[self.count - 1]
            self.label_coord_in_seis.setText(str(self.sou))
            self.dr = self.dict_data[self.sou]['dx']


    def change_clip(self, state):
        if state == Qt.Checked:
            self.clip = True
            self.update_graph()
        else:
            self.clip = False
            self.update_graph()


    def change_gane(self):
        self.gane = self.gane_spin.value()
        self.update_graph()


    def cut(self):

        self.dict_data = copy.deepcopy(self.dict_data_orig)
        self.dx = int(self.edit_receiver.text())
        self.L = int(self.edit_masw.text())
        if self.L > self.dict_data[self.sou]["rec_x"][-1]:
            return
        i = 0
        while (self.nx * self.dr - self.keys_data[i]) >= self.L:
            first_rec = self.keys_data[i] + self.dx
            last_rec = self.L + self.keys_data[i] + self.dx
            index_1sr_rec = int(first_rec // self.dr)
            index_last_rec = int(last_rec // self.dr)
            tmp_data = self.dict_data[self.keys_data[i]]['data'].T[index_1sr_rec:index_last_rec, :].T
            tmp_offset = self.dict_data[self.keys_data[i]]['rec_x'][index_1sr_rec:index_last_rec]
            self.dict_data_cut[self.keys_data[i]] = self.dict_data[self.keys_data[i]]
            self.dict_data_cut[self.keys_data[i]]['data'] = tmp_data
            self.dict_data_cut[self.keys_data[i]]['rec_x'] = tmp_offset
            i += 1
            if i >= len(self.keys_data): break
        self.dict_data = self.dict_data_cut
        self.keys_data = list(self.dict_data.keys())
        self.update_graph()


    def update_graph(self):
        self.seismograms_widget.canvas.axes.clear()
        self.draw(self.dict_data[self.keys_data[self.count - 1]])


    def threads_of_compute_spectr(self):
        self.button_compute_in_spectr.setEnabled(False)
        worker = Worker(self.compute_spectr)
        self.threadpool.start(worker)


    def compute_spectr(self):
        self.progressBar.setVisible(True)
        self.width = int(self.edit_weight.text())
        self.fmin = int(self.edit_fmin.text())
        self.fmax = int(self.edit_fmax.text())
        self.maxVel = int(self.edit_speed.text())
        self.spectr_count = 1
        self.keys_spectr = list(self.dict_data.keys())
        self.sou = self.keys_spectr[self.spectr_count - 1]
        self.label_coords_in_spectr.setText(str(self.sou))
        self.sou_desp = self.keys_spectr[0]

        self.curves[self.sou] = {}
        self.curves[self.sou][self.mod] = {}

        kr = len(self.dict_data)
        progress = 1
        ii = 0

        for key in self.dict_data.keys():
            ii+=1

            data = self.dict_data[key]['data']*seiswindow(self.dict_data[key]['data'], percdecay=50)

            fk2d, freq, k = SFK(data, self.dict_data[key]['dt'],
                                self.dict_data[key]['dx'],
                                fmin=self.fmin, fmax=self.fmax, offset0=0, multi_nt=4, multi_nr=40, width=0.2)
            vf2d = fk2vf(fk2d, freq, k, maxVel=self.maxVel, multi_k=50)[self.minVel:, :]

            self.dict_spectr[key] = {'fk2d': fk2d, 'freq': freq, 'k': k, 'vf2d': vf2d/np.max(vf2d, axis=0)}
            print('Source', str(ii)+'/'+str(kr))
            self.df = np.abs(freq[0] - freq[1])
            self.progressBar.setValue((progress/kr) * 100)
            progress += 1


        self.vf2d = self.dict_spectr[self.sou]['vf2d']
        self.dispersion.canvas.axes.clear()
        draw_spectr(self.dispersion.canvas.axes, self.dict_spectr[self.sou]['vf2d']**6, self.dict_spectr[self.sou]['freq'],
                    self.maxVel, self.minVel)
        self.dispersion.canvas.draw()
        self.dispersion.setVisible(True)
        self.toolbar2.setVisible(True)
        self.verticalSpacer_2.changeSize(20, 0)
        self.progressBar.setVisible(False)
        self.progressBar.setValue(0)
        self.button_compute_in_spectr.setEnabled(True)


    def next_spectr(self):
        if -1 < self.spectr_count < len(self.keys_data):

            if len(self.xs) != 0:
                if not (self.sou in self.curves):
                    self.curves[self.sou] = {}
                self.curves[self.sou][self.mod] = {'f': self.xs, 'V': self.ys}
                self.xs, self.ys = [], []

            self.spectr_count += 1
            self.sou_desp = self.keys_spectr[self.spectr_count - 1]
            self.sou = self.keys_spectr[self.spectr_count - 1]
            self.vf2d = self.dict_spectr[self.sou]['vf2d']
            self.label_coords_in_spectr.setText(str(self.sou))
            self.dispersion.canvas.axes.clear()
            draw_spectr(self.dispersion.canvas.axes, self.dict_spectr[self.sou]['vf2d'],
                        self.dict_spectr[self.sou]['freq'], self.maxVel, self.minVel)
            self.mod = 0
            self.dispersion.canvas.draw()
            self.update_spectr()
            self.spinBox.setValue(0)


    def prev_spectr(self):
        if self.spectr_count > 1:

            if len(self.xs) != 0:
                self.curves[self.sou][self.mod] = {'f': self.xs, 'V': self.ys}
                self.xs, self.ys = [], []

            self.spectr_count -= 1
            self.sou_desp = self.keys_spectr[self.spectr_count - 1]
            self.sou = self.keys_spectr[self.spectr_count - 1]
            self.vf2d = self.dict_spectr[self.sou]['vf2d']
            self.label_coords_in_spectr.setText(str(self.sou))
            self.dispersion.canvas.axes.clear()
            draw_spectr(self.dispersion.canvas.axes, self.dict_spectr[self.sou]['vf2d'],
                        self.dict_spectr[self.sou]['freq'], self.maxVel, self.minVel)
            self.mod = 0
            self.dispersion.canvas.draw()
            self.update_spectr()
            self.spinBox.setValue(0)


    def mouse_press(self, event):
        self.width = int(self.edit_weight.text())
        if event.inaxes == None: return

        if len(self.xs) == 0:
            ind_x = int((event.xdata-self.fmin) / self.df)
            ind_y_up = int((event.ydata + self.width) / self.dv)
            ind_y_down = int((event.ydata - self.width) / self.dv)
            ind_y_max = np.argmax(self.vf2d[ind_y_down:ind_y_up, ind_x])
            self.xs.append(event.xdata)
            self.ys.append(event.ydata - self.width + ind_y_max * self.dv)
            self.dispersion.canvas.axes.plot(self.xs, self.ys, c="r", marker='x', ms=5)
            self.dispersion.canvas.draw()
        else:
            if event.xdata > self.xs[-1]:
                ind_x = int((event.xdata-self.fmin) / self.df)
                ind_y_up = int((event.ydata + self.width) / self.dv)
                ind_y_down = int((event.ydata - self.width) / self.dv)
                ind_y_max = np.argmax(self.vf2d[ind_y_down:ind_y_up, ind_x])
                self.xs.append(event.xdata)
                self.ys.append(event.ydata - self.width + ind_y_max * self.dv)
                self.dispersion.canvas.axes.plot(self.xs, self.ys, c="r", marker='x', ms=5)
                self.dispersion.canvas.draw()
            else:
                pass

    def change_mod(self, state):
        if len(self.xs) != 0:
            if not (self.sou in self.curves):
                self.curves[self.sou] = {}
            self.curves[self.sou][self.mod] = {'f': self.xs, 'V': self.ys}
            self.xs, self.ys = [], []
        self.mod = state


    def delete_mode(self):
        try:
            del self.curves[self.sou][self.mod]
        except:
            print('For source ' + str(self.sou) + ' (m) ' + 'mode #' + str(self.mod), ' does not exist.')
        self.xs, self.ys = [], []
        self.update_spectr()


    def save(self):
        if len(self.xs) != 0:
            if not (self.sou in self.curves):
                self.curves[self.sou] = {}
            self.curves[self.sou][self.mod] = {'f': self.xs, 'V': self.ys, 'dx': self.dx, 'L': self.L}
        # if os.path.exists(self.curves_path):
        #     os.remove(self.curves_path)
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
        outfile = open(self.curves_path, 'wb')
        pickle.dump(self.curves, outfile)
        outfile.close()


    def update_spectr(self):
        self.dispersion.canvas.axes.clear()
        draw_spectr(self.dispersion.canvas.axes, self.dict_spectr[self.sou]['vf2d'], self.dict_spectr[self.sou]['freq'],
                    self.maxVel,self.minVel)
        try:
            for key in self.curves[self.sou]:
                self.dispersion.canvas.axes.plot(self.curves[self.sou][key]['f'], self.curves[self.sou][key]['V'], c="r", marker='x', ms=5)
                self.dispersion.canvas.draw()
        except:
            pass
        self.dispersion.canvas.draw()

    def save_inv_res(self, filename):
        outfile = open(filename, 'wb')
        res = {'vs': self.vs_rest, 'thk': self.thk_rest}
        pickle.dump(res, outfile)
        outfile.close()

    def compute_model(self):

        self.plot_xi = None
        self.dict_curv_old, self.keys_data, self.cmp = get_dict_curve(self.curves_path)
        self.sou_dc = self.keys_data[0]


        self.progressBar_2.setValue(0)
        self.progressBar_2.setVisible(True)
        for i in range(8):
            self.progressBar_2.setValue(i*10)
            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()

        self.is_xi_comp = True if self.xi == None else False

        self.vs_rest, self.thk_rest, self.dc_rest, self.freq, self.new_dc, self.mean_mode0, self.freq_mode0, \
        self.all_xi, self.xi, self.vs_rest_xi, self.thk_rest_xi, self.dc_rest_xi, self.model_range = \
        inversion_run(self.dict_curv_old, self.optimizer, self.num_use_modes)

        for i in range(2):
            self.progressBar_2.setValue(i*15 + 80)
            t = time.time()
            while time.time() < t + 0.1:
                app.processEvents()

        if self.optimizer == 'mc':

            self.save_inv_res('inversion_result_mc.pkl')

            if self.cbar != None: self.cbar.remove()
            self.model.canvas.axes.clear()
            self.model.canvas.axes.clear()
            if np.size(self.vs_rest,0) == 1:
                self.axis_1dmodel_mc()
                draw1dmodel(self.model.canvas.axes1, self.model.canvas.axes2, self.model_range,
                            self.vs_rest, self.thk_rest, self.new_dc, self.dc_rest, self.freq, self.num_use_modes, self.fontsize)
            else:
                self.vs2d, self.dep2d, self.cmp2d, self.nlay = get2dmodel(self.vs_rest, self.thk_rest, self.cmp)
                self.cbar = draw2dmodel(self.model.canvas.axes, self.vs2d, self.dep2d, self.cmp2d, self.nlay)
                self.change_dc()
                self.draw_dc()

            self.model.canvas.draw()
            # # self.change_xi()
            # # self.draw_xi()
            self.model.setVisible(True)
            # self.toolbar3.setVisible(True)
            # self.verticalSpacer_3.changeSize(20, 0)
            self.progressBar_2.setValue(100)
            self.progressBar_2.setVisible(False)

        if self.optimizer == 'gwo':

            self.save_inv_res('inversion_result_gwo.pkl')
            if self.cbar != None: self.cbar.remove()
            self.model_gwo.canvas.axes.clear()

            if np.size(self.vs_rest,0) == 1:

                self.axis_1dmodel_gwo()
                draw1dmodel(self.model_gwo.canvas.axes1, self.model_gwo.canvas.axes2, self.model_range,
                            self.vs_rest, self.thk_rest, self.new_dc, self.dc_rest, self.freq, self.num_use_modes,self.fontsize)
            else:
                self.vs2d, self.dep2d, self.cmp2d, self.nlay = get2dmodel(self.vs_rest, self.thk_rest, self.cmp)
                self.cbar_gwo = draw2dmodel(self.model_gwo.canvas.axes, self.vs2d, self.dep2d, self.cmp2d, self.nlay)
                self.change_dc_gwo()
                self.draw_dc_gwo()

            self.model_gwo.canvas.draw()
            self.change_xi_gwo()
            self.draw_xi_gwo()
            self.model_gwo.setVisible(True)
            self.toolbar4.setVisible(True)
            self.verticalSpacer_4.changeSize(20, 0)
            self.progressBar_2.setValue(100)
            self.progressBar_2.setVisible(False)
            self.cumpute_gwo.setEnabled(True)




    def draw_dc(self):

        for line in self.model.canvas.axes.lines: line.set_marker(None)
        self.sc_mc = self.model.canvas.axes.plot(self.cmp[self.dc_count-1], 0, 'v', mfc='k', mec='k', ms=10, clip_on=False, zorder=100)
        self.model.canvas.draw()
        self.plot_dc.label_coord_in_seis.setText(str(self.keys_data[self.dc_count - 1]))
        self.plot_dc.dc.canvas.axes1.clear()
        self.plot_dc.dc.canvas.axes2.clear()
        draw1dmodel(self.plot_dc.dc.canvas.axes1, self.plot_dc.dc.canvas.axes2, self.model_range, self.vs_rest[self.dc_count-1], self.thk_rest[self.dc_count-1],
                    self.new_dc[:, self.dc_count-1], self.dc_rest[self.dc_count-1, :], self.freq, self.num_use_modes, self.fontsize)
        self.plot_dc.dc.canvas.draw()

    def draw_dc_gwo(self):

        for line in self.model_gwo.canvas.axes.lines: line.set_marker(None)
        self.sc_mc = self.model_gwo.canvas.axes.plot(self.cmp[self.dc_count_gwo - 1], 0, 'v', mfc='k', mec='k', ms=10, clip_on=False, zorder=100)
        self.model_gwo.canvas.draw()
        self.plot_dc_gwo.label_coord_in_seis.setText(str(self.keys_data[self.dc_count_gwo - 1]))
        self.plot_dc_gwo.dc.canvas.axes1.clear()
        self.plot_dc_gwo.dc.canvas.axes2.clear()
        draw1dmodel(self.plot_dc_gwo.dc.canvas.axes1, self.plot_dc_gwo.dc.canvas.axes2, self.model_range, self.vs_rest[self.dc_count_gwo-1], self.thk_rest[self.dc_count_gwo-1],
                    self.new_dc[:, self.dc_count_gwo-1], self.dc_rest[self.dc_count_gwo-1, :], self.freq, self.num_use_modes, self.fontsize)
        self.plot_dc_gwo.dc.canvas.draw()


    def draw_xi_gwo(self):
        self.plot_xi_gwo.label_coord_in_seis.setText('Xi = ' + str(self.all_xi[self.xi_count_gwo - 1]))
        self.plot_xi_gwo.xi.canvas.axes1.clear()
        self.plot_xi_gwo.xi.canvas.axes2.clear()
        plot_model_vs_xi(self.xi_count_gwo  - 1, self.plot_xi_gwo.xi.canvas.axes1, self.plot_xi_gwo.xi.canvas.axes2,
                         self.plot_xi_gwo.xi.canvas.figure, self.vs_rest_xi, self.thk_rest_xi, self.dc_rest_xi,
                         self.freq_mode0, self.mean_mode0, self.vs2vp, self.dvs, self.wave, self.fontsize)
        self.plot_xi_gwo.xi.canvas.draw()

    def change_xi(self):
        self.plot_xi.xi.canvas.figure.delaxes(self.plot_xi.xi.canvas.axes)
        self.plot_xi.xi.canvas.axes1 = self.plot_xi.xi.canvas.figure.add_subplot(121)
        self.plot_xi.xi.canvas.axes2 = self.plot_xi.xi.canvas.figure.add_subplot(122)

    def change_dc(self):
        self.plot_dc.dc.canvas.figure.delaxes(self.plot_dc.dc.canvas.axes)
        self.plot_dc.dc.canvas.axes1 = self.plot_dc.dc.canvas.figure.add_subplot(121)
        self.plot_dc.dc.canvas.axes2 = self.plot_dc.dc.canvas.figure.add_subplot(122)

    def axis_1dmodel_mc(self):
        self.plot_dc = None
        self.model.canvas.figure.delaxes(self.model.canvas.axes)
        self.model.canvas.axes1 = self.model.canvas.figure.add_subplot(121)
        self.model.canvas.axes2 = self.model.canvas.figure.add_subplot(122)

    def axis_1dmodel_gwo(self):
        self.plot_dc_gwo = None
        self.model_gwo.canvas.figure.delaxes(self.model_gwo.canvas.axes)
        self.model_gwo.canvas.axes1 = self.model_gwo.canvas.figure.add_subplot(121)
        self.model_gwo.canvas.axes2 = self.model_gwo.canvas.figure.add_subplot(122)

    def change_xi_gwo(self):
        self.plot_xi_gwo.xi.canvas.figure.delaxes(self.plot_xi_gwo.xi.canvas.axes)
        self.plot_xi_gwo.xi.canvas.axes1 = self.plot_xi_gwo.xi.canvas.figure.add_subplot(121)
        self.plot_xi_gwo.xi.canvas.axes2 = self.plot_xi_gwo.xi.canvas.figure.add_subplot(122)

    def change_dc_gwo(self):
        self.plot_dc_gwo.dc.canvas.figure.delaxes(self.plot_dc_gwo.dc.canvas.axes)
        self.plot_dc_gwo.dc.canvas.axes1 = self.plot_dc_gwo.dc.canvas.figure.add_subplot(121)
        self.plot_dc_gwo.dc.canvas.axes2 = self.plot_dc_gwo.dc.canvas.figure.add_subplot(122)

    def draw_xi(self):
        self.plot_xi.label_coord_in_seis.setText('Xi = ' + str(self.all_xi[self.xi_count - 1]))
        self.plot_xi.xi.canvas.axes1.clear()
        self.plot_xi.xi.canvas.axes2.clear()
        plot_model_vs_xi(self.xi_count - 1, self.plot_xi.xi.canvas.axes1, self.plot_xi.xi.canvas.axes2,
                         self.plot_xi.xi.canvas.figure, self.vs_rest_xi, self.thk_rest_xi, self.dc_rest_xi,
                         self.freq_mode0, self.mean_mode0, self.vs2vp, self.dvs, self.wave, self.fontsize)
        self.plot_xi.xi.canvas.draw()

    def thread_complete(self):
        # print("THREAD COMPLETE!")
        if self.plot_xi != None:
            self.plot_xi.show()
        if self.plot_dc != None:
            self.plot_dc.show()

    def thread_complete_gwo(self):
        # print("THREAD COMPLETE!")
        self.plot_xi_gwo.show()
        if self.plot_dc_gwo != None:
            self.plot_dc_gwo.show()

    def threads_of_compute_model(self):
        self.pushButton.setEnabled(False)
        self.optimizer = 'mc'
        worker = Worker(self.compute_model)
        worker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(worker)

    def threads_of_compute_model_gwo(self):
        self.cumpute_gwo.setEnabled(False)
        self.optimizer = 'gwo'
        worker1 = Worker(self.compute_model)
        worker1.signals.finished.connect(self.thread_complete_gwo)
        self.threadpool.start(worker1)

class MovieSplashScreen(QSplashScreen):
    my_size = QSize(400, 300)

    def __init__(self, path_to_gif: str):
        self.movie = QMovie(path_to_gif)
        self.movie.jumpToFrame(0)
        pixmap = QPixmap(self.my_size)
        QSplashScreen.__init__(self, pixmap)
        self.movie.frameChanged.connect(self.repaint)

    def showEvent(self, event:PySide2.QtGui.QShowEvent) -> None:
        self.movie.start()

    def hideEvent(self, event:PySide2.QtGui.QHideEvent) -> None:
        self.movie.stop()

    def paintEvent(self, event:PySide2.QtGui.QPaintEvent) -> None:
        painter = QPainter(self)
        pixmap = self.movie.currentPixmap()
        pixmap = pixmap.scaled(self.my_size)
        painter.drawPixmap(0, 0, pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    progressbar_value = 30
    path_to_gif = 'icons\wgif.gif'

    splash = MovieSplashScreen(path_to_gif)
    progressbar = QProgressBar(splash)
    progressbar.setMaximum(progressbar_value)
    progressbar.setTextVisible(False)
    progressbar.setGeometry(0, splash.my_size.height() - 5,
                            splash.my_size.width(), 20)

    splash.show()

    for i in range(10):
        progressbar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()
    for i in range(10):
        progressbar.setValue(10)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()
    for i in range(6):
        progressbar.setValue(i*5+10)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    window = App()
    window.show()
    splash.finish(window)
    app.exec_()
