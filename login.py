import sys
import csv
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from detect import Ui_MainWindow
from datetime import datetime

class denglu(QWidget):
    """
    登录窗口 ：程序的入口
    登录窗口的内容包括两个tabel标签："账号"、"密码"，两个输入框分别用来输入账号及密码
    两个按钮：确定和退出，一个radiobutton用来设置密码的显示格式，一个显示标签用来创建新的账号
    密码在输入时应该默认为掩码输入，点击radiobutton时可以切换密码显示格式
    点击显示标签"创建新用户"时弹出创建窗口
    创建新账号时应该进行核查：账号不许为空不许重复，密码不许为空
    创建完成时把账号及密码存储在本地文件中：userInfo
    登录时应核查账号与密码的匹配，并根据各种出错情况给出相应的提示信息
    登陆成功时进入主页面并自动退出关闭登录窗口
    """
    def __init__(self):
        super(denglu, self).__init__()
        self.setGeometry(300, 300, 400, 247)
        #登录窗口无边界
        self.setWindowFlags(Qt.FramelessWindowHint)
        #登录窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #定义多个空label
        self.label_null1 = QLabel()
        self.label_null2 = QLabel()
        self.label_null3 = QLabel()
        self.label_null4 = QLabel()
        self.label_new = QLabel()
        #定义创建新账户标签并设置信号槽绑定事件
        self.label_new.setText("<a href='#'>注册新用户</a>")
        self.label_new.setStyleSheet('''color: rgb(253,129,53);''')
        self.label_new.linkActivated.connect(self.idnew)
        #设置隐藏密码RadioButton
        self.btn_check = QRadioButton("显示密码")
        self.btn_check.setStyleSheet('''color: rgb(253,129,53);;''')
        self.btn_check.clicked.connect(self.yanma)
        #登录与退出按钮，设置按钮颜色及事件绑定
        self.btn_denglu = QPushButton("登录")
        self.btn_quxiao = QPushButton("退出")
        self.btn_denglu.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_quxiao.setStyleSheet('''color: white;
                        background-color: rgb(218,181,150);''')
        self.btn_denglu.clicked.connect(self.check) #-------
        self.btn_quxiao.clicked.connect(self.quxiao)
        #账号和密码
        self.lineedit_id = QLineEdit()
        self.lineedit_id.setPlaceholderText("账号")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        self.lineedit_password.setPlaceholderText("密码")
        #布局设置
        layout = QHBoxLayout(self)
        wid_denglu_right = QWidget()
        wid_denglu_left = QLabel()
        g = QGridLayout()
        g.addWidget(self.lineedit_id, 1, 1, 1, 2)
        g.addWidget(self.lineedit_password, 2, 1, 1, 2)
        g.addWidget(self.btn_check, 3, 1)
        g.addWidget(self.btn_denglu, 4, 1)
        g.addWidget(self.btn_quxiao, 4, 2)
        g.addWidget(self.label_null1, 5, 1)
        g.addWidget(self.label_null2, 6, 1)
        g.addWidget(self.label_null3, 7, 1)
        g.addWidget(self.label_null4, 8, 1)
        g.addWidget(self.label_new, 9, 2 )
        wid_denglu_right.setLayout(g)
        layout.addWidget(wid_denglu_left)
        layout.addWidget(wid_denglu_right)
        self.setLayout(layout)
    #密码隐藏
    def yanma(self):
        if self.btn_check.isChecked():
            self.lineedit_password.setEchoMode(QLineEdit.Normal)
        else:
            self.lineedit_password.setEchoMode(QLineEdit.Password)
    #写入csv文件
    def user_message(self):
        USER_PWD = {}
        with open('userInfo.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                USER_PWD[row[0]] = row[1]
        return USER_PWD
    #登录时核查账号及密码是否正确
    def check(self):
        USER_PWD = self.user_message()
        #如果输入账号不在账号表文件中，则推送消息框提醒
        if self.lineedit_id.text() not in USER_PWD.keys():
            replay = QMessageBox.warning(self, "!", "账号或密码输入错误", QMessageBox.Yes)
        else:
            if USER_PWD.get(self.lineedit_id.text()) == self.lineedit_password.text():
                #账号密码验证成功，创建主界面，进入检测程序,并关闭登录窗口
                self.ui = Ui_MainWindow()
                self.ui.setupUi(mainWindow)
                mainWindow.show()
                self.close()
                self.save_log(self.lineedit_id.text())
            else:
                replay = QMessageBox.warning(self, "!", "账号或密码输入错误", QMessageBox.Yes)
    #存储日志文件
    def save_log(self, account):
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(account + '\t log in at ' + datetime.now().strftime('%y-%m-%d %I:%M:%S %p') + '\r')
            f.close()
    #创建新的账号
    def idnew(self):
        self.label_idnew_id = QLabel("账号")
        self.label_idnew_password = QLabel("密码")
        self.lineedit_idnew_id = QLineEdit()
        self.lineedit_idnew_password = QLineEdit()
        self.btn_idnew_quren = QPushButton("注册")
        self.btn_idnew_quren.clicked.connect(self.idnewqueren)
        self.btn_idnew_quxiao = QPushButton("取消")
        self.btn_idnew_quxiao.clicked.connect(self.idnewclose)
        self.idnew = QWidget()
        layout_idnew = QGridLayout()
        layout_idnew.addWidget(self.label_idnew_id, 1, 0)
        layout_idnew.addWidget(self.label_idnew_password, 2, 0)
        layout_idnew.addWidget(self.lineedit_idnew_id, 1, 1, 1, 2)
        layout_idnew.addWidget(self.lineedit_idnew_password, 2, 1, 1, 2)
        layout_idnew.addWidget(self.btn_idnew_quren, 3, 1)
        layout_idnew.addWidget(self.btn_idnew_quxiao, 3, 2)
        self.idnew.setLayout(layout_idnew)
        self.idnew.move(self.pos())
        self.idnew.resize(200, 133)
        self.idnew.setWindowFlags(Qt.FramelessWindowHint)
        self.paintEvent(self)
        self.idnew.setStyleSheet("background-color :rgb(253,216,174)")
        self.idnew.show()
    def save_message(self, account, pwd):
        headers = ['name', 'key']
        values = [{'name': account, 'key': pwd}]
        with open('userInfo.csv', 'a', encoding='utf-8', newline='') as fp:
            writer = csv.DictWriter(fp, headers)
            writer.writerows(values)
    #新账号注册的确认
    def idnewqueren(self):
        USER_PWD = self.user_message()
        if  self.lineedit_idnew_id.text() == "":
            replay = QMessageBox.warning(self, "!", "账号不准为空", QMessageBox.Yes)
        else:
            if self.lineedit_idnew_id.text() in USER_PWD.keys():
                replay = QMessageBox.warning(self, "!", "账号已存在", QMessageBox.Yes)
            else:
                if self.lineedit_idnew_password.text() == "":
                    replay = QMessageBox.warning(self, "!", "密码不准为空", QMessageBox.Yes)
                else:
                    self.save_message(self.lineedit_idnew_id.text(), self.lineedit_idnew_password.text())
                    replay = QMessageBox.warning(self, "!", "注册成功！", QMessageBox.Yes)
                    self.idnew.close()
    #添加背景图片
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("./denglu.jpg")
        painter.drawPixmap(self.rect(), pixmap)
    #关闭创新账号窗口
    def idnewclose(self):
        self.idnew.close()
    #取消创建新账号，并退出创建窗口
    def quxiao(self):
        sys.exit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    d = denglu()
    d.show()
    sys.exit(app.exec())