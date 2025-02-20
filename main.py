import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget
import sqlite3
from mainui import Ui_MainWindow
from addEditCoffeeFormUi import Ui_AddEditCoffeeForm


def create_database():
    conn = sqlite3.connect("data/coffee.sqlite")
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


class AddEditCoffeeForm(QWidget):
    def __init__(self, coffee_id=None):
        super().__init__()

        self.ui = Ui_AddEditCoffeeForm()
        self.ui.setupUi(self)

        self.coffee_id = coffee_id

        if coffee_id is not None:
            self.load_data()

    def load_data(self):
        conn = sqlite3.connect("data/coffee.sqlite")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        row = cursor.fetchone()

        self.ui.nameLineEdit.setText(row[1])
        self.ui.roastLevelLineEdit.setText(row[2])
        self.ui.grindLineEdit.setText(row[3])
        self.ui.tasteDescriptionLineEdit.setText(row[4])
        self.ui.priceLineEdit.setText(str(row[5]))
        self.ui.packageVolumeLineEdit.setText(str(row[6]))

        conn.close()

    def save_data(self):
        conn = sqlite3.connect("data/coffee.sqlite")
        cursor = conn.cursor()

        if self.coffee_id is None:
            cursor.execute("""
                INSERT INTO coffee (name, roast, type, description, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.ui.nameLineEdit.text(),
                self.ui.roastLevelLineEdit.text(),
                self.ui.grindLineEdit.text(),
                self.ui.tasteDescriptionLineEdit.text(),
                float(self.ui.priceLineEdit.text()),
                float(self.ui.packageVolumeLineEdit.text())
            ))
        else:
            cursor.execute("""
                UPDATE coffee
                SET name = ?, roast = ?, type = ?, description = ?, price = ?, volume = ?
                WHERE id = ?
            """, (
                self.ui.nameLineEdit.text(),
                self.ui.roastLevelLineEdit.text(),
                self.ui.grindLineEdit.text(),
                self.ui.tasteDescriptionLineEdit.text(),
                float(self.ui.priceLineEdit.text()),
                float(self.ui.packageVolumeLineEdit.text()),
                self.coffee_id
            ))

        conn.commit()
        conn.close()


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Espresso")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_data()

        self.ui.addCoffeeButton.clicked.connect(self.add_coffee)
        self.ui.editCoffeeButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        conn = sqlite3.connect("data/coffee.sqlite")
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

    def add_coffee(self):
        self.form = AddEditCoffeeForm()
        self.form.show()
        self.form.ui.saveButton.clicked.connect(self.form.save_data)
        self.form.ui.saveButton.clicked.connect(self.load_data)
        self.form.ui.saveButton.clicked.connect(self.form.close)

    def edit_coffee(self):
        row = self.ui.tableWidget.currentRow()
        if row != -1:
            coffee_id = int(self.ui.tableWidget.item(row, 0).text())
            self.form = AddEditCoffeeForm(coffee_id)
            self.form.show()
            self.form.ui.saveButton.clicked.connect(self.form.save_data)
            self.form.ui.saveButton.clicked.connect(self.load_data)
            self.form.ui.saveButton.clicked.connect(self.form.close)


if __name__ == "__main__":
    create_database()
    app = QApplication(sys.argv)
    window = Espresso()
    window.show()
    sys.exit(app.exec())
    