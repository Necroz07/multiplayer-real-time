import socket

ip = 'localhost'
port = 12345

x, y = 40, 15


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((ip, port))

def updatecoords(x, y, key, addr):
    if key == 'w' and y>1:
        y-=1
    elif key == 'a' and x>2:
        x-=2
    elif key == 's' and y<24:
        y+=1
    elif key == 'd' and x<76:
        x+=2

    coords=f"{x},{y}"
    server.sendto(coords.encode(), addr)
    print(f"new coords sent {x}, {y}")
    return x, y



print("Server is listening on port 12345...")

while True:
    data, addr = server.recvfrom(1024)
    key = data.decode()

    x, y= updatecoords(x, y, key, addr)
    