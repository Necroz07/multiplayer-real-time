import socket

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind(('localhost', 12345))

print("Server is listening on port 12345...")

while True:
    data, addr = server.recvfrom(1024)
    message= data.decode()
    print("accquired message from: {addr} with message: {message}")
    
