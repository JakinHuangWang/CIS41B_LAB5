import json
import socket
import sys
import numpy as np

HOST = 'localhost'
PORT = 6711
dataCount = 50
dataSize = 4096

if len(sys.argv) != 3:
    print("Has to be 2 arguments")
    raise SystemExit
else:
    print(str(sys.argv))
    
def printMinMaxY(someFunc):
    def wrapper(*args, **kwargs):
        XY = someFunc(*args, **kwargs)
        print(min(XY[1]), max(XY[1]))
        return XY
    return wrapper

@printMinMaxY
def getPower(data):
    power, minX, maxX = tuple([float(x) for x in data.split(',')])
    x = np.linspace(minX, maxX, dataCount)
    y = x ** power
    return [list(x), list(y), (power, minX, maxX)]

@printMinMaxY
def getSine(data):
    frequency = float(data)
    x = np.linspace(0, 1, dataCount)
    y = np.sin(frequency * 2 * np.pi * x)
    return [list(x), list(y), (frequency, )]

with socket.socket() as s:
    s.bind((HOST, PORT))
    print("Server hostname:", HOST, "port:", PORT)
    
    s.listen()
    (conn, addr) = s.accept()
    dataLst = []
    
    while True:
        fromClient = conn.recv(dataSize).decode('utf-8')
        if fromClient == 'q':
            break
        data = conn.recv(dataSize).decode('utf-8')
        if fromClient == 'p':
            dataLst = getPower(data)
        elif fromClient == 's':
            dataLst = getSine(data) 
        conn.send(json.dumps(dataLst).encode('utf-8'))
    

