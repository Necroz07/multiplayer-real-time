import socket, os, msvcrt, time, json

os.system("mode con: cols=85 lines=37")
ip = 'localhost'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def mapdraw(playerx, playery, width=78, height=26):
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
            

def sendcoords(key, playerid):
    msg = {"type":"key","playerid":f"{playerid}", "key":f"{key}"}
    client.sendto(json.dumps(msg).encode(), (ip, port))

def coordsextract(coords):
    coords=json.loads(coords.decode())
    x, y=data["x"], data["y"]
    return int(x), int(y)



user=input("Enter your name:\t")

join={"type":"join", "user":f"{user}"}
client.sendto(json.dumps(join).encode(), (ip, port))

data, addr = client.recvfrom(1024)
data=json.loads(data.decode())

playerid=data["playerid"]
x, y=int(data["x"]), int(data["y"])
mapdraw(x, y)



while True:

    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8").lower()
        if key in ('w', 'a', 's', 'd'):
            sendcoords(key, playerid)

            data, addr = client.recvfrom(1024)
            x, y= coordsextract(data)

    mapdraw(x, y)
    time.sleep(0.1)
  

    #print(f"The coordinates are ({x}, {y})")