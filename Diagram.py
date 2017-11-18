#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore,QtWidgets,QtGui
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class PlotWidget(FigureCanvas):
    def __init__(self, parent = None):

        self.figure = Figure(figsize=(6, 2), dpi=80, facecolor=(0.937, 0.937, 0.937))
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.x = np.arange(0.0, 3.0, 0.01)
        self.y = np.cos(2*np.pi*self.x)
        self.axes.plot(self.x, self.y)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        # FigureCanvas.setSizePolicy(self,
        #                            QtGui.QSizePolicy.Expanding,
        #                            QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)

class BigPlotWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.figure = Figure(figsize=(10, 6), dpi=80, facecolor=(0.937, 0.937, 0.937))
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)
        self.x = np.arange(0.0, 3.0, 0.01)
        self.y = np.cos(2 * np.pi * self.x)
        self.axes.plot(self.x, self.y)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        # FigureCanvas.setSizePolicy(self,
        #                            QtGui.QSizePolicy.Expanding,
        #                            QtGui.QSizePolicy.Expanding)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)