import socket

ip = 'localhost'
port = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((ip, port))

def updatecoords(x, y, addr):
    coords=f"{x},{y}"
    server.sendto(coords.encode(), addr)



print("Server is listening on port 12345...")

x, y= 0, 0

while True:
    data, addr = server.recvfrom(1024)
    key = data.decode()

    if key == 'w':
        y+=1
    elif key == 'a':
        x-=1
    elif key == 's':
        y-=1
    elif key == 'd':
        x+=1

    updatecoords(x, y, addr)
    