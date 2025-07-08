#SAMOGONER AE 3000 парсер данных 08.07.2025
#pip install chardet requests psycopg2-binary pandas matplotlib beautifulsoup4

import os
import time
import csv
import chardet
import requests
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from bs4 import BeautifulSoup

import config  # импортим секреты и URL из config.py

# Папка для CSV и графиков
ARCHIVE_FOLDER = "SMGNR"
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# Текущий CSV-файл (по дате)
current_day = datetime.now().strftime("%Y-%m-%d")
csv_file = os.path.join(ARCHIVE_FOLDER, f"data_log_{current_day}.csv")


def init_db():
    """Создать таблицу в базе, если ещё не создана."""
    conn = psycopg2.connect(
        host=config.PG_HOST,
        port=config.PG_PORT,
        dbname=config.PG_DB,
        user=config.PG_USER,
        password=config.PG_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS smgnLogs (
            timestamp           TIMESTAMP PRIMARY KEY,
            runtime_minutes     INTEGER,
            temperature_cube    REAL,
            temperature_cool    REAL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def write_to_db(data):
    """Записать один ряд данных в PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=config.PG_HOST,
            port=config.PG_PORT,
            dbname=config.PG_DB,
            user=config.PG_USER,
            password=config.PG_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO smgnLogs (timestamp, runtime_minutes, temperature_cube, temperature_cool)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (timestamp) DO NOTHING
        """, (
            data["timestamp"],
            data["runtime_minutes"],
            data["temperature_cube"],
            data["temperature_cool"]
        ))
        conn.commit()
        print(f"📥 Запись в БД: {data['timestamp']}")
    except Exception as e:
        print(f"[PostgreSQL ERROR] {e}. Данные записаны только в CSV.")
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass


def fetch_data():
    """Скачать и распарсить HTML со страницы платы."""
    try:
        resp = requests.get(config.URL, timeout=11)
        resp.raise_for_status()
        raw = resp.content
        enc = chardet.detect(raw)["encoding"] or "utf-8"
        html = raw.decode(enc, errors="replace")
        soup = BeautifulSoup(html, "html.parser")

        def extract(label):
            tag = soup.find(string=lambda t: t and label in t)
            if not tag:
                return None
            val = tag.split(":")[-1].strip()
            return val.rstrip("°C").strip()

        runtime = extract("Время работы")
        cube    = extract("В кубе")
        cool    = extract("Охлаждение")

        return {
            "timestamp":         datetime.now(),
            "runtime_minutes":   int(runtime.split()[0]) if runtime else None,
            "temperature_cube":  float(cube)  if cube  else None,
            "temperature_cool":  float(cool)  if cool  else None
        }
    except Exception as e:
        print(f"[ОШИБКА ПАРСИНГА] {e}")
        return None


def write_to_csv(data):
    """Добавить строку в CSV; при смене даты переключиться на новый файл."""
    global current_day, csv_file
    if data is None:
        return
    today = datetime.now().strftime("%Y-%m-%d")
    if today != current_day:
        current_day = today
        csv_file = os.path.join(ARCHIVE_FOLDER, f"data_log_{current_day}.csv")
    header = ["timestamp", "runtime_minutes", "temperature_cube", "temperature_cool"]
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow([
            data["timestamp"].strftime("%Y-%m-%d %H:%M:%S"),
            data["runtime_minutes"],
            data["temperature_cube"],
            data["temperature_cool"]
        ])
    print(f"📝 Запись в CSV: {csv_file}")


def save_temp_graph(csv_path, date_str):
    """Перестроить и сохранить график температур за указанный CSV-день."""
    try:
        df = pd.read_csv(csv_path, parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["temperature_cube"], label="Куб (°C)")
        plt.plot(df.index, df["temperature_cool"], label="Охлаждение (°C)")
        plt.xlabel("Время")
        plt.ylabel("Температура, °C")
        plt.title(f"Температуры за {date_str}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        graph_file = os.path.join(ARCHIVE_FOLDER, f"temp_graph_{date_str}.png")
        plt.savefig(graph_file)
        plt.close()
        print(f"[ГРАФИК] Сохранён: {graph_file}")
    except Exception as e:
        print(f"[ОШИБКА ГРАФИКА ТЕМП] {e}")


if __name__ == "__main__":
    # Пытаемся инициализировать БД, но при ошибке работаем только с CSV
    try:
        init_db()
    except Exception as e:
        print(f"[WARNING] Не удалось инициализировать БД: {e}. Все данные будут писаться в CSV.")

    while True:
        data = fetch_data()
        if data:
            write_to_csv(data)
            write_to_db(data)
            save_temp_graph(csv_file, current_day)
            time.sleep(60)  # ждать 60 секунд
        else:
            print("[ПОВТОР] Ошибка получения, через 30 сек")
            time.sleep(30)
