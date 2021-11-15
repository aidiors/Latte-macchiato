import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem


class DbReader(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.tableWidget.setGeometry(1, 1, 1890, 990)

        self.pole = ['ID', 'Name', 'Roasting', 'Ground', 'Description',
                     'Price', 'Volume']
        self.con = sqlite3.connect("coffee.sqlite")
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
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.add_row)
        self.pushButton_2.clicked.connect(self.edit)
        self.main = main

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DbReader()
    ex.show()
    sys.exit(app.exec_())
