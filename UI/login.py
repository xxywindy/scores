from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLineEdit, QListView, QVBoxLayout,  QFrame, QGraphicsOpacityEffect, QPushButton 
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import QRect
import json
from UI.query import *
from service.service import *

class zjuerLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 800)
        self._init_Ui()
        self.addfunciton()
        self.autologin()

    def _init_Ui(self):
        self.setWindowTitle('zjuer自动成绩查询')
        self.centerwidget = QWidget(self)
        # self.setWindowIcon(QIcon(''))                 # 图标地址
        palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap()))              # 图标地址
        self.setPalette(palette)
        self.setCentralWidget(self.centerwidget)

        self.listView = QListView(self.centerwidget)
        self.listView.setGeometry(QtCore.QRect(-5, 1, 1281, 771))
        self.listView.setStyleSheet("border-image: url(./images/background.png);")
        self.listView.setObjectName("listView")

        self.frame = QFrame(self.centerwidget)
        self.frame.setGeometry(460,280,360,480)
        self.frame.setStyleSheet("""  QFrame {  
        border-radius: 20px;  /* 设置圆角 */  
        background-color: rgba(128, 128, 128, 100);  /* 设置灰色半透明背景 */  }  """)  
        self.mainLayout = QVBoxLayout(self.frame)

        # 设置透明度
        op1 = QGraphicsOpacityEffect()
        op1.setOpacity(0.6)
        op2 = QGraphicsOpacityEffect()
        op2.setOpacity(0.6)
        op3 = QGraphicsOpacityEffect()
        op3.setOpacity(0.6)
        op4 = QGraphicsOpacityEffect()
        op4.setOpacity(0.8)
        op5 = QGraphicsOpacityEffect()
        op5.setOpacity(0.8)

        self.usernameEdit = QLineEdit(self)
        self.usernameEdit.setPlaceholderText('请输入您的学号')
        self.usernameEdit.setGraphicsEffect(op1)
        self.usernameEdit.setStyleSheet("QLineEdit{border-radius:5px;}")
        self.passwordEdit = QLineEdit(self)
        self.passwordEdit.setPlaceholderText('请输入您的密码')
        self.passwordEdit.setGraphicsEffect(op2)
        self.passwordEdit.setStyleSheet("QLineEdit{border-radius:5px;}")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.urlEdit = QLineEdit(self)
        self.urlEdit.setPlaceholderText('请输入您的钉钉机器人的url(选填)')
        self.urlEdit.setGraphicsEffect(op3)
        self.urlEdit.setStyleSheet("QLineEdit{border-radius:5px;}")

        self.loginbtn = QPushButton('登录')
        self.loginbtn.setGraphicsEffect(op4)
        self.loginbtn.setStyleSheet("QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
                                    QPushButton{font-family:'Arial';color:#FFFFFF;}")
        self.cancelbtn = QPushButton('退出')
        self.cancelbtn.setGraphicsEffect(op5)
        self.cancelbtn.setStyleSheet("QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
                                    QPushButton{font-family:'Arial';color:#FFFFFF;}")
        
        self.mainLayout.addWidget(self.usernameEdit)
        self.mainLayout.addWidget(self.passwordEdit)
        self.mainLayout.addWidget(self.urlEdit)
        self.mainLayout.addWidget(self.loginbtn)
        self.mainLayout.addWidget(self.cancelbtn)

        self.titleLab = QtWidgets.QLabel(self.centerwidget)
        self.titleLab.setGeometry(QRect(0, -50, 1280, 380))
        self.titleLab.setStyleSheet("font: 25 28pt \"Adobe 明體 Std L\";\n"
"font: 72pt \"字魂50号-白鸽天行体\";\n"
"color: rgb(36, 109, 243);")
        self.titleLab.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLab.setText('zjuer自动成绩查询')

    def addfunciton(self):
        self.loginbtn.clicked.connect(self.login)
        self.cancelbtn.clicked.connect(self.close)
        self.loginbtn.setShortcut(QtCore.Qt.Key_Return)

    def autologin(self):
        try:
            with open('database.json', 'r', encoding="utf-8") as f:
                userdata = json.load(f)
        except:
            return False
        if userdata.get('username') and userdata.get('password'):
            self.usernameEdit.setText(userdata.get('username'))
            self.passwordEdit.setText(userdata.get('password'))
            self.urlEdit.setText(userdata.get('url',None))
            return True
        return False

    def login(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        url = self.urlEdit.text()
        try:
            with open('database.json', 'r', encoding="utf-8") as f:
                userdata = json.load(f)
        except:
            userdata = {}
        userdata['username'] = username
        userdata['password'] = password
        userdata['url'] = url
        with open('database.json', 'w', encoding="utf-8") as load_f:
            load_f.write(json.dumps(userdata, indent=4, ensure_ascii=False))
        self.close()
        self.ui = zjuerQuery(User())
        self.ui.show()

if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    ui = zjuerLogin()
    ui.show()
    sys.exit(app.exec_())
