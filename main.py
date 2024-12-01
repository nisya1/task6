import sqlite3
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
from PyQt6 import uic
import sys
from main_interface import Ui_MainWindow as ui1
from addEditCoffeeForm import Ui_MainWindow as ui2


class AdminPanel(ui1, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = sqlite3.connect("data/coffee.sqlite").cursor()
        self.pushButton.clicked.connect(self.update_window)
        self.pushButton_2.clicked.connect(self.update_viev_table)
        self.return_table()

    def return_table(self):
        request = "SELECT * FROM 'coffee'"
        self.result = self.db.execute(request).fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена (руб.)", "Объем упаковки (гр)"])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.setColumnWidth(0, 30)
        self.tableWidget.setColumnWidth(1, 130)
        self.tableWidget.setColumnWidth(2, 110)
        self.tableWidget.setColumnWidth(3, 130)
        self.tableWidget.setColumnWidth(4, 280)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.setColumnWidth(6, 130)

    def update_window(self):
        self.wind = UpdateTable()
        self.wind.show()

    def update_viev_table(self):
        self.tableWidget.clear()
        request = "SELECT * FROM 'coffee'"
        self.result = self.db.execute(request).fetchall()
        self.tableWidget.setRowCount(len(self.result))
        self.tableWidget.setColumnCount(len(self.result[0]))
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена (руб.)",
             "Объем упаковки (гр)"])
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class UpdateTable(ui2, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = sqlite3.connect("data/coffee.sqlite")
        self.cur = self.db.cursor()

        self.tableWidget.itemChanged.connect(self.update_table)
        self.pushButton.clicked.connect(self.new_string)

        self.res = self.cur.execute("SELECT * from coffee").fetchall()
        self.tableWidget.setRowCount(len(self.res))
        self.tableWidget.setColumnCount(len(self.res[0]))

        self.tableWidget.setHorizontalHeaderLabels(
            ["id", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        for i, elem in enumerate(self.res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.res_db = {}
        for row, i in enumerate(self.res):
            for col, val in enumerate(i):
                col = ["id", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса", "цена",
                       "объем упаковки"][col]
                self.res_db[(int(row), col)] = val

    def update_table(self, item):
        try:
            col = ["id", "название сорта", "степень обжарки", "молотый/в зернах", "описание вкуса",
                                   "цена", "объем упаковки"][item.column()]
            if ((int(item.row()) + 1, col), item.text()) not in self.res_db.items():
                self.cur.execute(f"UPDATE coffee SET '{col}'='{item.text()}' WHERE id=?", (int(item.row() + 1),))
            self.db.commit()
        except Exception as e:
            pass

    def new_string(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QTableWidgetItem(str(self.tableWidget.rowCount())))
        self.db.execute("INSERT INTO coffee(id) VALUES (?)", (self.tableWidget.rowCount(),))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AdminPanel()
    ex.show()
    sys.exit(app.exec())