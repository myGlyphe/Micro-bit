#!/usr/bin/env python
import sqlite3
import os

def setup():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE readings (date text, time text, temperature int, light_level int)")
    conn.commit()
    conn.close()

def log_reading(payload):
    checking()
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings VALUES (?,?,?,?)", (str(payload["date"]), str(payload["time"]), int(payload["temperature"]), int(payload["light_level"])))
    conn.commit()
    conn.close()

def get_readings():
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    logs = []
    for row in cursor.execute("SELECT * FROM readings ORDER BY date DESC, time DESC LIMIT 40"):
        logs.append(row)
    conn.commit()
    conn.close()
    return logs

def checking():
    if not os.path.exists("./logs.db"):
        setup()

if __name__ == "__main__":
    checking()