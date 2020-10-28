# Micro-bit
Reading levels on microbit and displaying/logging

OS REQUIRED: Windows 7 (or higher)
Python Version REQUIRED: 3.x (or higher)
PIP Required

To run, simply create a virtual environment using `py -m venv /path/to/new/virtual/environment` 
and then to invoke environment run `py -m venv c:\path\to\myenv` or run the activate.bat file inside the Scripts folder in the environment.
To install dependencies run `py -m pip install -r requirements.txt`, make sure you're located inside the /src folder.

Createthe database by running `py database.py`
To recreate the database, simply delete the file `logs.db` and run `py database.py` again.

Start the webserver using `py app.py` or `flask run`.

The included shell.py is a Python file to interact with the database using raw SQL inputs.

Features include:
  Temperature and light level readings from Microbit using USB serial.
  Displaying these readings on a webapp created through Python using Flask.
  Updating information in realtime using flask-socketio for websocket and jQuery for client development.
  Logging high values and every hour to a database created using sqlite3 for python.
  Alerting user when high temperature or light level is read.
  Possibility to use any async-mode (gevent default).
  Displays latency between server and client.
  Simple user-interace for ease of use with buttons to navigate through pages.
