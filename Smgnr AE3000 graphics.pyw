# SAMOGONER AE 3000 графики разгонки 09.07.2025
# pip install PyQt5 psycopg2-binary pandas matplotlib

import sys
import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QMessageBox, QDateEdit,
    QFileDialog, QCheckBox
)
from PyQt5.QtCore import QDate

import config  # PG_HOST, PG_PORT, PG_DB, PG_USER, PG_PASSWORD

class TempPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График температур")
        self.setGeometry(300, 300, 500, 200)
        self.df = None
        self.current_dir = None
        self.init_ui()
        self.check_db_availability()

    def init_ui(self):
        layout = QVBoxLayout()

        # Даты
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("С:"))
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.start_date)

        date_layout.addWidget(QLabel("По:"))
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        date_layout.addWidget(self.end_date)

        layout.addLayout(date_layout)

        # Чекбокс
        self.save_checkbox = QCheckBox("Сохранять график при построении")
        self.save_checkbox.setChecked(False)
        layout.addWidget(self.save_checkbox)

        # Загрузка из CSV
        self.load_csv_btn = QPushButton("Загрузить из CSV")
        self.load_csv_btn.clicked.connect(self.load_and_plot_csv)
        layout.addWidget(self.load_csv_btn)

        # Загрузка из БД
        self.load_db_btn = QPushButton("Загрузить из БД")
        self.load_db_btn.clicked.connect(self.load_and_plot_db)
        layout.addWidget(self.load_db_btn)

        self.setLayout(layout)

    def check_db_availability(self):
        try:
            conn = psycopg2.connect(
                host=config.PG_HOST,
                port=config.PG_PORT,
                dbname=config.PG_DB,
                user=config.PG_USER,
                password=config.PG_PASSWORD,
                connect_timeout=3
            )
            conn.close()
        except Exception:
            self.load_db_btn.setEnabled(False)
            QMessageBox.warning(
                self,
                "База данных недоступна",
                "Не удалось подключиться к PostgreSQL.\n"
                "Будет доступна только загрузка из CSV."
            )

    def load_and_plot_db(self):
        start_str = self.start_date.date().toString("yyyy-MM-dd") + " 00:00:00"
        end_str   = self.end_date.date().toString("yyyy-MM-dd")   + " 23:59:59"
        try:
            conn = psycopg2.connect(
                host=config.PG_HOST,
                port=config.PG_PORT,
                dbname=config.PG_DB,
                user=config.PG_USER,
                password=config.PG_PASSWORD,
                connect_timeout=5
            )
            query = """
                SELECT timestamp, temperature_cube, temperature_cool
                FROM smgnLogs
                WHERE timestamp BETWEEN %s AND %s
                ORDER BY timestamp
            """
            df = pd.read_sql(query, conn, params=(start_str, end_str), parse_dates=["timestamp"])
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка подключения к БД", str(e))
            return

        if df.empty:
            QMessageBox.information(
                self,
                "Нет данных",
                f"Нет записей за период {start_str[:10]} – {end_str[:10]}."
            )
            return

        df.set_index("timestamp", inplace=True)
        self.df = df
        self.plot_temp(f"с_{start_str[:10]}_по_{end_str[:10]}")

    def load_and_plot_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выбрать CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            df = pd.read_csv(path, parse_dates=["timestamp"])
            df.set_index("timestamp", inplace=True)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка чтения CSV", str(e))
            return

        if df.empty:
            QMessageBox.information(self, "Пустой CSV", "Выбранный файл не содержит данных.")
            return

        self.df = df
        # запомним папку для автосохранения
        self.current_dir = os.path.dirname(path)
        filename = os.path.basename(path)
        self.plot_temp(f"CSV_{filename}")

    def plot_temp(self, title_suffix=""):
        if self.df is None or self.df.empty:
            QMessageBox.information(self, "Нет данных", "Нет данных для отображения.")
            return

        plt.figure(figsize=(10, 5))
        plt.plot(self.df.index, self.df["temperature_cube"], label="Куб (°C)")
        plt.plot(self.df.index, self.df["temperature_cool"], label="Охлаждение (°C)")
        plt.xlabel("Время")
        plt.ylabel("Температура, °C")
        plt.title(f"Температуры {title_suffix}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # автосохранение, если чекбокс установлен
        if self.save_checkbox.isChecked():
            filename = f"temperatures_{title_suffix}.png"
            if self.current_dir:
                out_path = os.path.join(self.current_dir, filename)
            else:
                out_path = filename
            plt.savefig(out_path, dpi=300)
            QMessageBox.information(self, "Сохранено", f"График сохранён в\n{out_path}")

        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TempPlotter()
    win.show()
    sys.exit(app.exec_())
