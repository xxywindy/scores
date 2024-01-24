from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QRadioButton, QLineEdit, QMessageBox
  
from service.service import *
from math import ceil

class MyQueryTable(QWidget):
    control_signal = pyqtSignal(list)

    def __init__(self, user, lst = ['选课课号','课程名称','学分','成绩','绩点','补考成绩']):
        super().__init__()
        self.user = user
        self.lst = lst
        self.newTableWidget()
        self.addfunciton()

    def newTableWidget(self):
        self.VResLayout = QVBoxLayout(self)

        self.HQueryLayout = QHBoxLayout()
        self.YearComboBox = QComboBox()
        self.YearComboBox.addItem("")
        self.YearComboBox.setItemText(0,"全部")
        self.YearComboBox.addItem("")
        self.YearComboBox.setItemText(1,"2022-2023")
        self.YearComboBox.addItem("")
        self.YearComboBox.setItemText(2,"2023-2024")
        self.YearComboBox.addItem("")
        self.YearComboBox.setItemText(3,"2024-2025")
        self.YearComboBox.addItem("")
        self.YearComboBox.setItemText(4,"2025-2026")
        self.SemesterComboBox = QComboBox()
        self.SemesterComboBox.addItem("")
        self.SemesterComboBox.setItemText(0,"全部")
        self.SemesterComboBox.addItem("")
        self.SemesterComboBox.setItemText(1,"春、夏")
        self.SemesterComboBox.addItem("")
        self.SemesterComboBox.setItemText(2,"秋、冬")
        self.MajorButton = QRadioButton()
        self.MajorButton.setText('只看主修')
        self.QueryButton = QPushButton()
        self.QueryButton.setText('查询')
        self.HQueryLayout.addWidget(self.YearComboBox)
        self.HQueryLayout.addWidget(self.SemesterComboBox)
        self.HQueryLayout.addWidget(self.MajorButton)
        self.HQueryLayout.addWidget(self.QueryButton)
        self.VResLayout.addLayout(self.HQueryLayout)

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(len(self.lst))
        self.tableWidget.setHorizontalHeaderLabels(self.lst)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 使列表自适应宽度
        self.tableWidget.verticalHeader().setSectionResizeMode(6)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)    # 设置tablewidget不可编辑
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)      # 设置tablewidget不可选中
        self.VResLayout.addWidget(self.tableWidget)
        # 默认页数为1
        self.pagecontrol = self.setPageController(1)

    def addfunciton(self):
        self.QueryButton.clicked.connect(self.querybtn)
        self.control_signal.connect(self.page_controller)
        self.MajorButton.clicked.connect(self.major)
        self.YearComboBox.currentIndexChanged[int].connect(self.year)  # 条目发生改变，发射信号，传递条目索引
        self.SemesterComboBox.currentIndexChanged[int].connect(self.semester)  # 条目发生改变，发射信号，传递条目索引

    def setPageController(self, page):          # 总页数为page
        """自定义页码控制器"""
        control_layout = QHBoxLayout()
        homePage = QPushButton("首页")
        prePage = QPushButton("<上一页")
        self.curPage = QLabel("1")
        nextPage = QPushButton("下一页>")
        finalPage = QPushButton("尾页")
        self.totalPage = QLabel("共" + str(page) + "页")
        skipLable_0 = QLabel("跳到")
        self.skipPage = QLineEdit()
        skipLabel_1 = QLabel("页")
        confirmSkip = QPushButton("确定")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.VResLayout.addLayout(control_layout)

    # 查询按钮点击事件
    def querybtn(self):
        self.query(1)
        # 当前页面赋值为1
        self.curPage.setText("1")

    # 成绩查询函数
    def query(self,page=1):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()    # 清空tablewidger中的内容，不包括表头
        self.tableWidget.verticalHeader().setVisible(False)   # 隐藏行表头
        res = self.user.ScoreQuery(page)
        self.UpdateTotalPage(self.TotalPage())
        if res:
            x = 0
            for i in res:
                row_num = self.tableWidget.rowCount()#获取当前的行数
                self.tableWidget.setRowCount(row_num + 1)#添加一行
                y = 0
                # for j in i:    # 感觉这种写法不太安全,因为数据库列数会多于该列数
                # 同样的,表格最后一行应该会放置按钮,所以事实上后面会设置少放置一列
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(res[x][y])))
                    y = y + 1
                x = x + 1
    
    # 年份选择事件
    def year(self,year):
        if year == 0:
            self.user.year = ''
        elif year == 1:
            self.user.year = "AND year = '2022-2023'"
        elif year == 2:
            self.user.year = "AND year = '2023-2024'"
        elif year == 3:
            self.user.year = "AND year = '2024-2025'"
        elif year == 4:
            self.user.year = "AND year = '2025-2026'"
    
    # 学期选择事件
    def semester(self,semester):
        if semester == 0:
            self.user.semester = ''
        elif semester == 1:
            self.user.semester = "AND semester = '春夏'"
        elif semester == 2:
            self.user.semester = "AND semester = '秋冬'"

    # 单选框点击事件
    def major(self):
        if self.sender().isChecked() == True:
            self.user.major = "AND major = 'Y'"
        else:
            self.user.major = ''

    # 修改总页数
    def UpdateTotalPage(self,page):
        if page != 0:
            self.totalPage.setText("共" + str(page) + "页")
        else:
            self.totalPage.setText("共1页")

    # 返回总页数
    def TotalPage(self):
        # 9条信息分一页
        # table是sql语句
        res = self.user.CountQuery()
        page = ceil(res[0][0]/LIMIT)
        return page

    # 页码控制器
    def page_controller(self, signal):
        total_page = self.showTotalPage()
        if "home" == signal[0]:
            self.curPage.setText("1")
        elif "pre" == signal[0]:
            if 1 == int(signal[1]):
                QMessageBox.information(None, "提示", "已经是第一页了", QMessageBox.Yes)
                return
            self.curPage.setText(str(int(signal[1]) - 1))
        elif "next" == signal[0]:
            if total_page == int(signal[1]):
                QMessageBox.information(None, "提示", "已经是最后一页了", QMessageBox.Yes)
                return
            self.curPage.setText(str(int(signal[1]) + 1))
        elif "final" == signal[0]:
            self.curPage.setText(str(total_page))
        elif "confirm" == signal[0]:
            if signal[1] == '':
                QMessageBox.information(None, "提示", "未选择页码", QMessageBox.Yes)
                return
            if total_page < int(signal[1]) or int(signal[1]) < 0:
                QMessageBox.information(None, "提示", "跳转页码超出范围", QMessageBox.Yes)
                return
            self.curPage.setText(signal[1])

        self.changeTableContent()  # 改变表格内容

    def changeTableContent(self):
        """根据当前页改变表格的内容"""
        cur_page = self.curPage.text()
        self.query(int(cur_page))

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])
        
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = MyQueryTable(User())
    win.show()
    sys.exit(app.exec_())