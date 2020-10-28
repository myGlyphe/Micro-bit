#!/usr/bin/env python
from threading import Lock, Thread
from flask import Flask, render_template, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit

import serial
import microbit
import database
from datetime import datetime

async_mode = None

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

lastHighLog = {}
totalReadings = 0
lastLog = 0
conn = serial.Serial()

def background_thread():
    global totalReadings
    global lastLog
    while True:
        try:
            port = microbit.get_microbit()
            if not port:
                socketio.emit("temp_lightlevel", {"temp": "MICROBIT NOT FOUND", "light": "MICROBIT NOT FOUND"}, namespace="/test")
                conn.close()
                socketio.sleep(2)
                continue
            conn.baudrate = 115200
            conn.port = port
            conn.open()
            x = conn.readline()
            varab = x.decode()[:28]
            varab = varab.split()
            for i in varab:
                if i == " ":
                    list.remove(i)
            varab = "".join(varab)
            result = varab.split(",")
            now = datetime.now()
            date = str(now.strftime("%d/%m/%Y"))
            time = str(now.strftime("%H:%M:%S"))
            if int(result[1]) > 200 or int(result[0]) > 30:
                print("WARNING! Hight levels")
                try:
                    if len(lastHighLog) == 0 or lastHighLog["date"] != date or lastHighLog["hour"] != time.split(":")[0]:
                        lastHighLog["date"] = date
                        lastHighLog["hour"] = time.split(":")[0]
                        to_send = {}
                        to_send["date"] = date
                        to_send["time"] = time
                        to_send["temperature"] = int(result[0])
                        to_send["light_level"] = int(result[1])
                        database.log_reading(to_send)
                        logs = database.get_readings()
                        socketio.emit("append_logs", logs, namespace="/test")
                        socketio.emit("my_response",
                            {"data": "WARNING! High levels"}, namespace="/test")
                except KeyError:
                    lastHighLog["date"] = date
                    lastHighLog["hour"] = time.split(":")[0]
                    logs = database.get_readings()
                    socketio.emit("append_logs", logs, namespace="/test")
                    socketio.emit("my_response",
                        {"data": "WARNING! High levels"}, namespace="/test")
            socketio.emit("temp_lightlevel", {"temp": str(int(result[0]) - 4), "light": str(result[1])}, namespace="/test")
            if totalReadings - lastLog >= 1300 or totalReadings == 0:
                to_send = {}
                to_send["date"] = date
                to_send["time"] = time
                to_send["temperature"] = int(result[0])
                to_send["light_level"] = int(result[1])
                database.log_reading(to_send)
                lastLog = totalReadings
                logs = database.get_readings()
                socketio.emit("append_logs", logs, namespace="/test")
                print("logging current reading")
            conn.close()
            totalReadings += 1
            socketio.sleep(2)
        except serial.SerialException as e:
            socketio.emit("temp_lightlevel", {"temp": "MICROBIT NOT FOUND", "light": "MICROBIT NOT FOUND"}, namespace="/test")
            conn.close()
            socketio.sleep(2)

@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)

@app.route("/logs")
def logs():
    return render_template("logs.html", async_mode=socketio.async_mode)

@socketio.on("get_logs", namespace="/test")
def get_logs():
    logs = database.get_readings()
    emit("append_logs", logs)

@socketio.on("my_ping", namespace="/test")
def ping_pong():
    emit("my_pong")

if __name__ == "__main__":
    socketio.start_background_task(background_thread)
    socketio.run(app, debug=True)