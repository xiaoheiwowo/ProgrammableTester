# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

from matplotlib.ticker import FormatStrFormatter
from matplotlib import patheffects

from public.datacache import SoftwareData as sw


class PlotWidget(FigureCanvas):
    """
    绘图
    """

    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 5), dpi=80, facecolor='none')
        self.cvs = FigureCanvas(self.fig)
        self.ax = self.fig.add_axes([0.02, 0.2, 0.85, 0.8])
        # 设置图标内背景颜色
        self.ax.set_facecolor('none')

        # 设置图表边框颜色，位置
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_position(('data', 0))
        self.ax.spines['top'].set_color('black')
        self.ax.spines['bottom'].set_position(('data', 0))
        # 坐标轴数值位置
        self.ax.xaxis.set_ticks_position('bottom')
        self.ax.yaxis.set_ticks_position('right')

        # 添加文本 阴影
        # self.text = self.ax.text(-1, 1,
        #                          'BD3S',
        #                          fontsize=18,
        #                          path_effects=[patheffects.withSimplePatchShadow()])

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # notify the system of updated policy
        FigureCanvas.updateGeometry(self)
        # 点击交互
        # self.cid = self.fig.canvas.mpl_connect('button_press_event', self.fig_press)

    def fig_press(self, event):
        """
        点击图像交互
        :param event:
        :return:
        """
        print('you pressed', event.button, event.xdata, event.ydata)
        if self.line_valve:
            self.line_valve.remove()
        if self.v_line:
            self.v_line.remove()
        # 添加线
        self.v_line = self.ax.axvline(event.xdata, color='lime', ls='--')
        # 注解
        for i in range(len(self.ar_data_show_x)):
            if event.xdata < self.ar_data_show_x[i]:
                break

        self.line_valve = self.ax.annotate(str(self.ar_data_show[i]) + 'mA',
                                           (event.xdata, max(self.ar_data_show)),
                                           xycoords='data',
                                           xytext=(20, 0),
                                           textcoords='offset points',
                                           fontsize=16,
                                           color='lime',
                                           arrowprops=dict(arrowstyle='-|>',
                                                           connectionstyle="arc3,rad=.2",
                                                           color='lime')
                                           )
        FigureCanvas.draw_idle(self)

    def update_diagram(self, yy, myflag=1):
        """
        更新曲线
        :param yy:
        :param myflag=1: myflag = 0 主界面小窗口
        :return:
        """
        self.interval = sw.current_set['data_interval'] / 1000
        self.ar_data_show = yy
        self.ax.clear()
        xx = []
        for i in range(len(yy)):
            xx.append((-1 * len(yy) + 1 + i) * self.interval)
        self.ar_data_show_x = xx
        # 绘制线，设置属性
        self.line2d = self.ax.plot(xx,
                                   yy,
                                   linewidth=1,
                                   color='r',
                                   label='Current',
                                   ls='-',
                                   marker='',
                                   mec='r',
                                   mfc='r',
                                   ms=6,
                                   # path_effects=[patheffects.SimpleLineShadow(),
                                   #                patheffects.Normal()]
                                   )
        # 设置坐标轴限值
        self.ax.set_xlim(right=0)
        self.ax.set_ylim(bottom=0, top=1100)#max(yy) * 1.2 + 0.00001)
        self.ax.yaxis.tick_right()
        # Y坐标保留两位小数
        # self.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

        # 网格
        # self.ax.grid()
        # 图表
        if myflag:
            rowLabels = ['Mod', 'Vol', 'Cur']
            tableVal = [['BD3S'], ['DC5V'], ['200mA']]
            self.myTable = self.ax.table(cellText=tableVal,
                                         colWidths=[0.08] * 3,
                                         rowLabels=rowLabels,
                                         colLabels=['Valve'],
                                         loc='upper right')

            # Title & Label
            self.ax.set_title('Current Curve')
        else:
            # limit_x = sw.current_set['small_win_show_time'] * 1000 / sw.current_set['data_interval']
            # text1 = self.ax.text(-limit_x, 0,
            #                      'ms',
            #                      fontsize=12,
            #                      path_effects=[patheffects.withSimplePatchShadow()])
            pass
        # self.ax.legend(loc=2, ncol=1)
        self.ax.yaxis.set_label_position('right')
        self.ax.set_xlabel('T/s', fontsize=12, labelpad=3)
        self.ax.set_ylabel('I/mA', fontsize=12, labelpad=3)

        self.v_line = self.ax.axvline(0.01, color='none', ls='--')
        self.line_valve = self.ax.annotate('D', (0, 0), color='none')
        self.draw()

    def save_picture(self, name):
        """
        保存图片
        :return:
        """
        self.fig.savefig(name[:-1], dpi=80)

    def turn_on_cid(self):
        """
        打开点击功能
        :return:
        """

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.fig_press)
        return self.cid

    def turn_off_cid(self, cid):
        """
        关闭点击功能
        :param cid:
        :return:
        """

        self.fig.canvas.mpl_disconnect(cid)
