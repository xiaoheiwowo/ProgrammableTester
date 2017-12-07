# 记事本
##
### 20171206
# plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']#用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
# myfont = matplotlib.font_manager.FontProperties(fname='simhei.ttf')

self.fig = Figure(figsize=(8, 5), dpi=80, facecolor='gray') # facecolor为图表外背景色
        self.cvs = FigureCanvas(self.fig)
        self.ax = self.fig.add_axes([0.02, 0.12, 0.92, 0.8])#self.fig.add_subplot(111)
        self.ax.set_facecolor('none')
        # 双y轴
        # self.myFigure1 = self.myFigureno.twinx()
        self.x_init = xx#np.arange(-10.0, 0, 0.05)
        self.y_init = yy#10 * (np.cos(2 * np.pi * self.x_init) + 1)
        # 添加线
        # self.myFigure1.axvline(-2)
        # 设置线属性
        self.line2d = self.ax.plot(xx, yy)

        # self.myFigure1.plot(self.x_init,
        #                     self.y_init,
        #                     linewidth=1.5,
        #                     color='r',
        #                     label='Current',
        #                     ls='-',
        #                     marker='o',
        #                     mec='r',
        #                     mfc='r',
        #                     ms=6,
        #                     path_effects=[patheffects.SimpleLineShadow(),
        #                                   patheffects.Normal()]
        #                     )
        # self.myFigure1.set_xdata(range(20))
        # self.myFigure1.set_y(np.random.rand(20))
        # 设置图标内背景颜色
        self.ax.set_facecolor('none')
        # 设置坐标轴限值
        self.ax.set_xlim(right=0)
        self.ax.set_ylim(bottom=0)
        self.ax.yaxis.tick_right()

        # Title & Label
        # self.myFigure1.set_title('vvv')
        self.ax.yaxis.set_label_position('right')
        self.ax.set_xlabel('T/s', fontsize=12, labelpad=3)
        self.ax.set_ylabel('I/mA', fontsize=12, labelpad=3)
        # 图表
        rowLabels = ['Mod', 'Vol', 'Cur']
        tableVal = [['BD3S'],['DC5V'],['200mA']]
        self.myTable = self.ax.table(cellText=tableVal,
                                     colWidths=[0.08] * 3,
                                     rowLabels=rowLabels,
                                     colLabels=['Valve'],
                                     loc='upper right')
        # 图例
        self.ax.legend(loc=2, ncol=1)
        # self.myFigure1.legend(loc=2, ncol=1, mode='expand', bbox_to_anchor=(0.0, 0.8, 1, 0.102))
        # 注解
        # self.myFigure1.annotate(r'$\cos(\frac{2\pi}{3})=-\frac{1}{2}$', (-10, 0.5), xycoords='data', xytext=(2, 1),
        #                         textcoords='offset points', fontsize=16,
        #                         arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2"))
        # 设置图表边框颜色，位置
        self.ax.spines['left'].set_color('none')
        # self.myFigure1.spines['right'].set_position(('data', 1.5))
        self.ax.spines['top'].set_color('none')
        # self.myFigure1.spines['bottom'].set_position(('data', 0))
        # 坐标轴数值位置
        self.ax.xaxis.set_ticks_position('bottom')
        # self.myFigure1.yaxis.set_ticks_position('right')
        # 调整边框
        # self.fig.subplots_adjust(0.02, 0.12, 0.92, 0.96)
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

        self.liney = self.ax.axvline(0, color='none', ls='--')
        self.notey = self.ax.annotate('D', (0, 0), color='none')


    def on_press(self, event):
        """
        点击图像交互
        :param event:
        :return:
        """
        print('you pressed', event.button, event.xdata, event.ydata)
        # self.notey._wrap()
        self.notey.remove()
        self.liney.remove()
        self.liney = self.ax.axvline(event.xdata, color='w', ls='--')
        self.notey = self.ax.annotate(str(round(event.ydata, 2)) + 'mA',
                                      (event.xdata, 16),
                                      xycoords='data',
                                      xytext=(20, 20),
                                      textcoords='offset points',
                                      fontsize=16,
                                      color='lime',
                                      arrowprops=dict(arrowstyle='-|>',
                                                      connectionstyle="arc3,rad=.2",
                                                      color='lime'))
        FigureCanvas.draw_idle(self)
matplotlib动态图
import matplotlib.animation as animation

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
