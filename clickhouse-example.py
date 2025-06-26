from clickhouse_driver import Client
import json

# Подключение к серверу Clickhouse
client = Client(host='localhost',  # Use 'localhost' or '127.0.0.1' for a local server
                user='default',    # Default user, adjust if you've changed the user
                password='',       # Default installation has no password for 'default' user
                port=9000)

# Создание БД если она не существует
client.execute('CREATE DATABASE IF NOT EXISTS town_cary')

# Создание таблицы
# Создание основной таблицы 'crashes'
client.execute('''
    CREATE TABLE IF NOT EXISTS town_cary.crashes (
    id UInt64,
    location_description String,
    rdfeature String,
    rdsurface String,
    rdcondition String,
    lightcond String,
    weather String,
    crash_date Int64,
    year String,
    fatalities String,
    injuries String,
    month String
    ) ENGINE = MergeTree

    ORDER BY id;
    ''')
print("Таблица создана успешно.")