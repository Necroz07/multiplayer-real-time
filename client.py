import socket
import os
import msvcrt
import time

os.system("mode con: cols=80 lines=30")
ip = 'localhost'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x, y = 40, 15


def map(playerx, playery, width=78, height=26):
    os.system('cls')
    board=""
    for y in range(height):
        for x in range(width):
            if x==playerx and y==playery:
                board+="X"
            elif x==0 or x==(width-1):
                board+="|"
            elif y==0 or y==(height-1):
                board+="—"
            else:
                board+=" "
        board+="\n"
    print(board, end="")
            
            




def sendcoords(key):
    msg = f"{key}"
    print(msg)
    client.sendto(msg.encode(), (ip, port))

def coordsextract(coords):
    coords=coords.decode()
    x, y= coords.split(',')
    return int(x), int(y)


while True:

    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8").lower()
        if key in ('w', 'a', 's', 'd'):
            sendcoords(key)

            coords, addr = client.recvfrom(1024)
        x, y= coordsextract(coords)

    map(x, y)
    time.sleep(0.1)


    

    #print(f"The coordinates are ({x}, {y})")





