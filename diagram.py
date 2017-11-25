#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore,QtWidgets,QtGui
import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['MS Reference Sans Serif']#用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# myfont = matplotlib.font_manager.FontProperties(fname=r'C:/Windows/Fonts/adobemingstd-light.otf')
from matplotlib.figure import Figure
from matplotlib import patheffects
import matplotlib.animation as animation




class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xx=[], yy=[]):
        self.fig = Figure(figsize=(8, 5), dpi=80, facecolor='gray') # facecolor为图表外背景色
        self.canvas = FigureCanvas(self.fig)
        self.myFigure1 = self.fig.add_subplot(111)
        self.myFigure1.set_facecolor('none')
        # 双y轴
        # self.myFigure1 = self.myFigureno.twinx()
        self.myFigure1.set_ylabel('I/mA',fontsize=12, labelpad=3)
        self.x_init = xx#np.arange(-10.0, 0, 0.05)
        self.y_init = yy#10 * (np.cos(2 * np.pi * self.x_init) + 1)
        # 添加线
        # self.myFigure1.axvline(-2)
        # 设置线属性
        self.myFigure1.plot(self.x_init, self.y_init, linewidth=1.5, color='r', label='Current', ls='-', marker='o', mec='r', mfc='r', ms=6
                            , path_effects=[patheffects.SimpleLineShadow(),patheffects.Normal()])
        # self.myFigure1.set_xdata(range(20))
        # self.myFigure1.set_y(np.random.rand(20))
        # 设置图标内背景颜色
        self.myFigure1.set_facecolor('none')
        # 设置坐标轴限值
        self.myFigure1.set_xlim(right=0)
        self.myFigure1.set_ylim(bottom=0)
        self.myFigure1.yaxis.tick_right()

        # Title & Label
        # self.myFigure1.set_title('vvv')
        self.myFigure1.yaxis.set_label_position('right')
        self.myFigure1.set_xlabel('T/s', fontsize=12, labelpad=3)
        self.myFigure1.set_ylabel('I/mA', fontsize=12, labelpad=3)
        # 图表
        rowLabels = ['Mod', 'Vol', 'Cur']
        tableVal = [['BD3S'],['DC5V'],['200mA']]
        self.myTable = self.myFigure1.table(cellText=tableVal,
                                       colWidths=[0.08] * 3,
                                       rowLabels=rowLabels,
                                       colLabels=['Valve'],
                                       loc='upper right')
        # 图例
        self.myFigure1.legend(loc=2, ncol=1)
        # self.myFigure1.legend(loc=2, ncol=1, mode='expand', bbox_to_anchor=(0.0, 0.8, 1, 0.102))
        # 注解
        # self.myFigure1.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$', (-10, 0.5), xycoords='data', xytext=(2, 1),
        #                         textcoords='offset points', fontsize=16,
        #                         arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
        # 设置图表边框颜色，位置
        self.myFigure1.spines['left'].set_color('none')
        # self.myFigure1.spines['right'].set_position(('data', 1.5))
        self.myFigure1.spines['top'].set_color('none')
        # self.myFigure1.spines['bottom'].set_position(('data', 0))
        # 坐标轴数值位置
        self.myFigure1.xaxis.set_ticks_position('bottom')
        # self.myFigure1.yaxis.set_ticks_position('right')
        # 调整边框
        self.fig.subplots_adjust(0.02, 0.12, 0.92, 0.96)
        # 网格
        # self.myFigure1.grid(which='major', axis='both')
        # 添加文本 阴影
        # self.text = self.myFigure1.text(-1,1,'BD3S',fontsize=18,path_effects=[patheffects.withSimplePatchShadow()])
        # 保存
        # self.figure.savefig('name.png', dpi=80)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_press)

        self.liney = self.myFigure1.axvline(0, color='none', ls='--')
        self.notey = self.myFigure1.annotate('D', (0, 0), color='none')


    def on_press(self, event):
        print('you pressed', event.button, event.xdata, event.ydata)
        # self.notey._wrap()
        self.notey.remove()
        self.liney.remove()
        self.liney = self.myFigure1.axvline(event.xdata, color='w', ls='--')
        self.notey = self.myFigure1.annotate(str(round(event.ydata, 2))+'mA', (event.xdata, 16),
                                xycoords='data', xytext=(20, 20),
                                textcoords='offset points', fontsize=16,
                                color='lime',
                                arrowprops=dict(arrowstyle='-|>', connectionstyle="arc3,rad=.2",color='lime'))
        FigureCanvas.draw_idle(self)



class DrawDiagram(QtWidgets.QWidget):
    def __init__(self, parent=None, XInput=[0], YInput=[0]):
        super(DrawDiagram, self).__init__(parent)

        self.dynamicBegin()
        self.x = XInput
        self.y = YInput

        self.Picture1 = PlotWidget(self)

    def dynamicBegin(self):
        self.ani = animation.FuncAnimation(self.Picture1.figure, self.animate, blit=True, interval=1000)

    def dynamicStop(self):
        self.ani._stop()

    def animate(self, i):
        self.x = range(-50,0)
        self.y = np.random.rand(50)
        return self.myFigure1.plot(self.x, self.y, linewidth=1.5, color='r', label='Current', ls='-', marker='o',
                            mec='r', mfc='r', ms=6,
                            path_effects=[patheffects.SimpleLineShadow(), patheffects.Normal()])


