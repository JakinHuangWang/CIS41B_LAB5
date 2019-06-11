import json
import socket
import numpy as np
import matplotlib.pyplot as plt

HOST = '127.0.0.1'
PORT = 6711
dataSize = 4096

menu = '''p: power function\ns: sine function\nq: quit\nEnter Choice: '''
powerPrompt = '''Enter exponent, minX, maxX: '''
sinePrompt = '''Enter frequency: '''


def Plot(dataLst):
    x, y, A = dataLst[0], dataLst[1], dataLst[2]
    plt.plot(x, y, "-r")
    if len(A) == 1:
        plt.title("Sine%.2fx" % (float(A[0])))
    else:
        plt.title("x^%.2f for x = %.2f to %.2f" % (float(A[0]), float(A[1]), float(A[2])))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    return min(y), max(y)

def prompt(someMenu):
    return input(someMenu).strip().lower()

def isValidInput(mesg):
    try:
        for x in mesg.split(','):float(x)
        return True
    except ValueError:
        return False
    
with socket.socket() as s:
    s.connect((HOST, PORT))
    print("Client connect to:", HOST, "port:", PORT)

    mesg = prompt(menu)
    s.send(mesg.encode('utf-8'))                   
    while mesg != 'q':
        if mesg == 'p' or mesg == 's':
            if mesg == 'p':
                mesg = prompt(powerPrompt)
                while not isValidInput(mesg):
                    mesg = input("Please Enter Another exponent, minX, maxX: ")
            else:
                mesg = prompt(sinePrompt)
                while not isValidInput(mesg):
                    mesg = input("Please Enter Another Frequency: ")
            s.send(mesg.encode('utf-8'))               
            Plot(json.loads(s.recv(dataSize).decode('utf-8')))
        mesg = prompt(menu)
        s.send(mesg.encode('utf-8'))               
        
        


