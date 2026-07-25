import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

x= int(input("Enter the x coordinate:\t"))

y= int(input("Enter the y coordinate:\t"))

msg = f"Player 1 is at ({x},{y})"

client.sendto(msg.encode(), ('localhost', 12345))
print("message sent, please check the server terminal.")