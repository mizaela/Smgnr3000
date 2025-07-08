Скрипты Smgnr AE3000 для работы с контроллером самогонного аппарата SAMOGONER AE 3000 https://github.com/malyshevars/samogoner (ESP8266, HW-364A) 

Smgnr AE3000 parser.py

Периодически запрашивает HTML-страницу контроллера,
Парсит из неё значения «Время работы», «Температура в кубе» и «Температура охлаждения»,
Сохраняет записи в CSV-файл (SMGNR/data_log_YYYY-MM-DD.csv),
Пытается записать данные в таблицу smgnLogs PostgreSQL, при ошибках с базой — только в CSV,
Генерирует и сохраняет график температур (SMGNR/temp_graph_YYYY-MM-DD.png).

Smgnr AE3000 tester.pyw 

PyQt5-панель тестирования: вручную задаёт параметры (режим, T₁, T₂, уровень liq, состояние термостата) и отправляет HTTP-запросы к контроллеру (использует curl через subprocess), отображая ответ устройства.

Smgnr AE3000 graphics.pyw

Небольшое GUI-приложение на PyQt5,
Позволяет выбрать диапазон дат и подгрузить данные либо из CSV, либо напрямую из БД,
Строит интерактивный график температур с помощью Matplotlib.

![Smgnr gui](https://github.com/user-attachments/assets/ef3870fa-f044-4d92-91e1-91bb2a3b0081)

Установка зависимостей:
Python 3.8+
pip install chardet requests beautifulsoup4 psycopg2-binary pandas matplotlib PyQt5
