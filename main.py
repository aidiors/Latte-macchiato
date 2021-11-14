import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.tableWidget.setGeometry(1, 1, 1890, 990)

        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(len(cur.execute("""SELECT id FROM coffee""").fetchall()))
        self.tableWidget.setHorizontalHeaderLabels(
            ['ID', 'Name', 'Roasting', 'Ground', 'Description',
             'Price', 'Volume'])
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for index, data in enumerate(cur.execute(f"""SELECT * FROM coffee""").fetchall()):
            for i, inf in enumerate(data):
                item = QTableWidgetItem(str(inf))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.tableWidget.setItem(index, i, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
