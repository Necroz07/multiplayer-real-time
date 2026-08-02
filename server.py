import socket, json, random

ip = 'localhost'
port = 12345

spawnable_x, spawnable_y = 40, 15
score=""

playerid=-1
players={}
clients={}


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((ip, port))

def updatecoords(players, playerid, key, addr):

    x=int(players[id]["x"])
    y=int(players[id]["y"])

    if key == 'w' and y>1:
        y-=1
    elif key == 'a' and x>2:
        x-=2
    elif key == 's' and y<24:
        y+=1
    elif key == 'd' and x<76:
        x+=2

    players[playerid]["x"]=str(x)
    players[playerid]["y"]=str(y)


    send_state(players, playerid, addr)



def send_state(players, playerid, addr):
    msg = {"type":"state", "yourid":str(playerid), "players":players}
    server.sendto((json.dumps(msg)).encode(), addr)
    




def initialize(players, spawnable_x, spawnable_y): 
    collision=False
    while True:
        spawnable_x= random.randint(2, 76)
        spawnable_y= random.randint(1, 24)

        for i in players:
            while (spawnable_x==players[i]["x"] and spawnable_y==players[i]["y"]):
                collision=True
                break
        
        if not collision:
            return spawnable_x, spawnable_y
                 


print("Server is listening on port 12345...")

while True:

    data, addr = server.recvfrom(1024)
    data = json.loads(data.decode())
    if data["type"]=="join":
        
        user = data["user"]

        playerid+=1

        spawnable_x, spawnable_y = initialize(players, spawnable_x, spawnable_y)

        players[playerid]= {
                            "user":f"{user}", 
                            "x":f"{spawnable_x}",
                            "y":f"{spawnable_y}",
                            "score":str(0)
                            }
        
        clients[playerid]=addr
        print("New player joined", playerid)

        send_state(players, playerid, addr)
        


    if data["type"]=="key":
        print("key update recieved")
        id=int(data["playerid"])
        updatecoords(players, id, data["key"], addr)



# STATE UPDATE
    if clients:

        for pid, addr in clients.items():
            send_state(players, pid, addr)
            
            print("state update for", playerid)