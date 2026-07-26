import socket
import os
import msvcrt

os.system("mode con: cols=100 lines=15")
ip = 'localhost'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x, y = 0, 0


def sendcoords(key):
    msg = f"{key}"
    print(msg)
    client.sendto(msg.encode(), (ip, port))

def coordsextract(coords):
    coords=coords.decode()
    x, y= coords.split(',')
    return x, y


while True:

    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8").lower()        
        sendcoords(key)

        coords, addr = client.recvfrom(1024)
        x, y= coordsextract(coords)

    print(f"The coordinates are ({x}, {y})")



