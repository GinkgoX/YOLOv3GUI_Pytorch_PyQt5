import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import *
from pyqt5.yolov3.util import *
import torch
import time
from pyqt5.yolov3.cam_demo import write, prep_image, arg_parse
from pyqt5.yolov3.darknet import Darknet
from pyqt5.yolov3.preprocess import prep_image


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1042, 921)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 显示摄像头画面
        self.cam_frame = QtWidgets.QFrame(self.centralwidget)
        self.cam_frame.setGeometry(QtCore.QRect(10, 110, 521, 571))
        self.cam_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cam_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cam_frame.setObjectName("cam_frame")

        self.label_img_show = QtWidgets.QLabel(self.cam_frame)
        self.label_img_show.setGeometry(QtCore.QRect(10, 10, 501, 551))
        self.label_img_show.setObjectName("label_img_show")
        # self.label_img_show.setStyleSheet(("border:2px solid red"))

        # 显示检测画面
        self.detect_frame = QtWidgets.QFrame(self.centralwidget)
        self.detect_frame.setGeometry(QtCore.QRect(540, 110, 491, 571))
        self.detect_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.detect_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.detect_frame.setObjectName("detect_frame")
        self.label_detect_show = QtWidgets.QLabel(self.detect_frame)
        self.label_detect_show.setGeometry(QtCore.QRect(10, 10, 481, 551))
        self.label_detect_show.setObjectName("label_detect_show")
        # self.label_detect_show.setStyleSheet(("border:2px solid green"))
        # 按钮框架
        self.btn_frame = QtWidgets.QFrame(self.centralwidget)
        self.btn_frame.setGeometry(QtCore.QRect(10, 20, 1021, 80))
        self.btn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.btn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.btn_frame.setObjectName("frame_3")

        # 按钮水平布局
        self.widget = QtWidgets.QWidget(self.btn_frame)
        self.widget.setGeometry(QtCore.QRect(20, 10, 1000, 60))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 20, 20, 10)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
  
        # 打开摄像头
        self.btn_opencam = QtWidgets.QPushButton(self.widget)
        self.btn_opencam.setObjectName("btn_opencam")
        self.horizontalLayout.addWidget(self.btn_opencam)
        # 加载模型文件
        self.btn_model_add_file = QtWidgets.QPushButton(self.widget)
        self.btn_model_add_file.setObjectName("btn_model_add_file")
        self.horizontalLayout.addWidget(self.btn_model_add_file)
        # 加载cfg文件
        self.btn_cfg_add_file = QtWidgets.QPushButton(self.widget)
        self.btn_cfg_add_file.setObjectName("btn_cfg_add_file")
        self.horizontalLayout.addWidget(self.btn_cfg_add_file)
        # 开始检测
        self.btn_detect = QtWidgets.QPushButton(self.widget)
        self.btn_detect.setObjectName("btn_detect")
        self.horizontalLayout.addWidget(self.btn_detect)
        # 退出
        self.btn_exit = QtWidgets.QPushButton(self.widget)
        self.btn_exit.setObjectName("btn_exit")
        self.horizontalLayout.addWidget(self.btn_exit)

        #定义帮助文档并设置信号槽绑定事件
        self.label_doc = QtWidgets.QLabel(self.centralwidget)
        self.label_doc.setText("<a href='#'>帮助文档</a>")
        self.label_doc.setStyleSheet('''color: rgb(253,129,53);''')
        self.label_doc.setGeometry(QtCore.QRect(900, 400, 800, 551))

        self.content = QtWidgets.QTextBrowser(self.centralwidget)
        self.content.setGeometry(QtCore.QRect(20, 660, 500, 200))

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1042, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # 这里将按钮和定义的动作相连，通过click信号连接openfile槽
        # 加载模型文件
        self.btn_model_add_file.clicked.connect(self.open_model)
        # 加载cfg文件
        self.btn_cfg_add_file.clicked.connect(self.open_cfg)
        # 打开摄像头
        self.btn_opencam.clicked.connect(self.opencam)
        # 开始识别
        self.btn_detect.clicked.connect(self.detect)
        # 这里是将btn_exit按钮和Form窗口相连，点击按钮发送关闭窗口命令
        self.btn_exit.clicked.connect(MainWindow.close)
        #帮助文档
        self.label_doc.linkActivated.connect(self.help_doc)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "目标检测"))

        self.label_img_show.setText(_translate("MainWindow", "摄像头原始画面"))
        self.label_detect_show.setText(_translate("MainWindow", "实时检测效果"))
        self.btn_opencam.setText(_translate("MainWindow", "打开摄像头"))
        self.btn_model_add_file.setText(_translate("MainWindow", "加载模型文件"))
        self.btn_cfg_add_file.setText(_translate("MainWindow", "加载cfg文件"))
        self.btn_detect.setText(_translate("MainWindow", "开始检测"))
        self.btn_exit.setText(_translate("MainWindow", "退出"))

    def open_model(self):
        global openfile_name_mdoel
        openfile_name_mdoel, _ = QFileDialog.getOpenFileName(self.btn_model_add_file, '选择模型文件',
                                                             'pyqt5/yolov3/')
        print('加载模型文件地址为：' + str(openfile_name_mdoel))

    def open_cfg(self):
        global openfile_name_cfg
        openfile_name_cfg, _ = QFileDialog.getOpenFileName(self.btn_cfg_add_file, '选择cfg文件',
                                                           'pyqt5/yolov3/')
        print('加载cfg文件地址为：' + str(openfile_name_cfg))

    def opencam(self):
        self.camcapture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer()
        self.timer.start()
        self.timer.setInterval(3)  # 0.1s刷新一次
        self.timer.timeout.connect(self.camshow)

    def camshow(self):
        # global self.camimg
        _, self.camimg = self.camcapture.read()
        camimg = cv2.cvtColor(self.camimg, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(camimg.data, camimg.shape[1], camimg.shape[0], QtGui.QImage.Format_RGB888)
        self.label_img_show.setPixmap(QtGui.QPixmap.fromImage(showImage))

    def detect(self):
        self.frames = 0
        self.start = time.time()
        cfgfile = openfile_name_cfg
        weightsfile = openfile_name_mdoel
        self.num_classes = 80
        args = arg_parse()
        self.confidence = float(args.confidence)
        self.nms_thesh = float(args.nms_thresh)
        self.CUDA = True

        self.model = Darknet(cfgfile)
        self.model.load_weights(weightsfile)

        self.model.net_info["height"] = args.reso
        self.inp_dim = int(self.model.net_info["height"])
        assert self.inp_dim % 32 == 0
        assert self.inp_dim > 32
        self.timerdec = QtCore.QTimer()
        self.timerdec.start()
        self.timerdec.setInterval(3)  # 0.1s刷新一次
        self.timerdec.timeout.connect(self.object_detection)

    def object_detection(self):
        if self.CUDA:
            self.model.cuda()
        self.model.eval()
        img, orig_im, dim = prep_image(self.camimg, self.inp_dim)
        output = self.model(Variable(img).cuda(), self.CUDA)
        output = write_results(output, self.confidence, self.num_classes, nms=True, nms_conf=self.nms_thesh)
        output[:, 1:5] = torch.clamp(output[:, 1:5], 0.0, float(self.inp_dim)) / self.inp_dim
        output[:, [1, 3]] *= self.camimg.shape[1]
        output[:, [2, 4]] *= self.camimg.shape[0]
        list(map(lambda x: write(x, orig_im), output))
        self.frames += 1
        print("FPS of the video is {:5.2f}".format(self.frames / (time.time() - self.start)))
        camimg = cv2.cvtColor(self.camimg, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(camimg.data, camimg.shape[1], camimg.shape[0], QtGui.QImage.Format_RGB888)
        self.label_detect_show.setPixmap(QtGui.QPixmap.fromImage(showImage))
        QApplication.processEvents()
    
    #创建新的账号
    def help_doc(self):
        #1 加载txt文件
        print("load--text")
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
            with f:
                data = f.read()
                # self.content.setText(data)
                self.content.setHtml(data)

def DetectMain():
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    # 向主窗口上添加控件
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    DetectMain()

