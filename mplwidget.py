import matplotlib.pyplot as plt
from PySide2.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
import matplotlib
    
class MplWidget(QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.figure = Figure()
        matplotlib.rcParams["toolbar"] = 'None'
        self.figure.patch.set_facecolor((79/255., 79/255., 79/255.))
        self.canvas = FigureCanvas(self.figure)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        