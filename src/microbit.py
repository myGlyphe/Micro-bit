import serial

conn = serial.Serial()
conn.baudrate = 115200
conn.timeout = .5

def get_microbit():
    for x in range(1, 10):
        try:
            conn.port = "COM" + str(x)
            conn.open()
            conn.write("\n".encode("utf-8"))
            new = conn.read_until(b"microbitfound                 \r\n")
            try:
                if new.decode().startswith("microbitfound"):
                    conn.close()
                    return "COM" + str(x)
            except UnicodeDecodeError:
                continue
        except serial.SerialException as e:
            continue
    return False