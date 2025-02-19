import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6 import uic
import sqlite3


def create_database():
    conn = sqlite3.connect("coffee.sqlite")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            roast TEXT NOT NULL,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            volume REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Espresso")

        self.ui = uic.loadUi("main.ui", self)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.ui.tableWidget.setRowCount(len(rows))
        self.ui.tableWidget.setColumnCount(7)

        headers = ["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах",
                   "Описание вкуса", "Цена", "Объем упаковки"]
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
        conn.close()


if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = Espresso()
    window.show()
    sys.exit(app.exec())
