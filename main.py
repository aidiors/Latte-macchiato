from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QMainWindow
import sys
import sqlite3


class DbReader(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 1000)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        self.tableWidget.setGeometry(1, 1, 1890, 990)

        self.pole = ['ID', 'Name', 'Roasting', 'Ground', 'Description',
                     'Price', 'Volume']
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.con.cursor()
        self.tableWidget.setColumnCount(7)
        self.row_count = len(self.cur.execute("""SELECT id FROM coffee""").fetchall())
        self.tableWidget.setRowCount(self.row_count)
        self.tableWidget.setHorizontalHeaderLabels(self.pole)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for index, data in enumerate(self.cur.execute(f"""SELECT * FROM coffee""").fetchall()):
            for i, inf in enumerate(data):
                item = QTableWidgetItem(str(inf))
                self.tableWidget.setItem(index, i, item)
        self.tableWidget.itemDoubleClicked.connect(self.add_edit_dialog)

    def add_edit_dialog(self):
        self.add_edit = AddEdit(self)
        self.add_edit.show()


class AddEdit(QMainWindow):
    def __init__(self, main):
        super().__init__()
        self.resize(776, 219)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(0, 20, 771, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(70, 160, 241, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.spinBox = QtWidgets.QSpinBox(self)
        self.spinBox.setGeometry(QtCore.QRect(0, 130, 60, 22))
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self)
        self.spinBox_2.setGeometry(QtCore.QRect(0, 180, 60, 22))
        self.spinBox_2.setMaximum(1000000000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 110, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(0, 160, 51, 16))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(70, 140, 51, 16))
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 771, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(0, 80, 771, 20))
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(320, 122, 451, 91))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton.clicked.connect(self.add_row)
        self.pushButton_2.clicked.connect(self.edit)
        self.main = main

        self.pushButton.setText("Добавить запись о кофе")
        self.label.setText("Row")
        self.label_2.setText("Column")
        self.label_3.setText("Text")
        self.label_4.setText("Добавить запись")
        self.label_5.setText("Изменить")
        self.pushButton_2.setText("Изменить")

    def add_row(self):
        self.main.cur.execute("""INSERT INTO coffee(Name) VALUES ('None')""")
        self.main.con.commit()
        self.main.row_count += 1
        self.main.tableWidget.setRowCount(self.main.row_count)
        for index, data in enumerate(self.main.cur.execute(f"""SELECT * FROM coffee""").fetchall()):
            for i, inf in enumerate(data):
                item = QTableWidgetItem(str(inf))
                self.main.tableWidget.setItem(index, i, item)

    def edit(self):
        text = self.lineEdit.text()
        r, c = self.spinBox.value(), self.spinBox_2.value()
        idi = self.main.tableWidget.item(r, 0).text()
        if text and c > 0:
            column = self.main.pole[c]
            self.main.cur.execute(f"""UPDATE coffee
SET {column} = ?
WHERE ID = ?;""", (text, idi))
            self.main.con.commit()
            self.main.tableWidget.setItem(r, c, QTableWidgetItem(text))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = DbReader()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())