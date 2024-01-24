from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QListView, QVBoxLayout, QFrame
from qfluentwidgets import LineEdit, PushButton, PasswordLineEdit
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import QRect
from UI.query import *
from service.service import *
from images.resources import *
import json

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
        palette = QPalette()
        self.setPalette(palette)
        self.setCentralWidget(self.centerwidget)

        self.listView = QListView(self.centerwidget)
        self.listView.setGeometry(QtCore.QRect(-5, 1, 1281, 771))
        self.listView.setStyleSheet("border-image: url(:/images/background.png);")
        self.listView.setObjectName("listView")

        self.frame = QFrame(self.centerwidget)
        self.frame.setGeometry(390,280,500,480)
        self.frame.setStyleSheet("""  QFrame {  
            border-radius: 20px;  /* 设置圆角 */  
            background-color: rgba(128, 128, 128, 0.4);  /* 设置灰色半透明背景 */ 
            padding-top: 30px;
            padding-left: 80px;
            padding-bottom: 30px;
            padding-right: 80px;
            margin-bottom: 80px
        }""")  
        self.mainLayout = QVBoxLayout(self.frame)

        # 设置透明度

        self.usernameEdit = LineEdit(self)
        self.usernameEdit.setPlaceholderText('请输入您的学号')
        self.usernameEdit.setStyleSheet("LineEdit{border-radius:5px;}")
        self.passwordEdit = PasswordLineEdit(self)
        self.passwordEdit.setPlaceholderText('请输入您的密码')
        self.passwordEdit.setStyleSheet("LineEdit{border-radius:5px;}")
        self.urlEdit = LineEdit(self)
        self.urlEdit.setPlaceholderText('请输入您的钉钉机器人的url(选填)')
        self.urlEdit.setStyleSheet("LineEdit{border-radius:5px;}")

        self.loginbtn = PushButton('登录')
        self.cancelbtn = PushButton('退出')
        
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
