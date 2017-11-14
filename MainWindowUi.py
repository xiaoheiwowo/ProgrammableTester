from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setWindowTitle('可编程测试仪')
        # MainWindow.setMaximumSize(QtCore.QSize(1920, 1080)) #不设置最大值可以使用最大化按钮

        # 菜单栏
        self.MenuBar = QtWidgets.QMenuBar(self)
        self.MenuBar.setObjectName('MenuBar')
        self.Menu = QtWidgets.QMenu(self.MenuBar)

        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName('ActionControlSet')
        self.Menu.addAction(self.action1)
        MainWindow.setMenuBar(self.MenuBar)



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.Menu.setTitle(_translate('MainWindow', '设置'))

# import images.image_rc