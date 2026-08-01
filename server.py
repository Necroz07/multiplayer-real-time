import socket, json, random

ip = 'localhost'
port = 12345

spawnable_x, spawnable_y = 40, 15
score=""

playerid=-1
players={}


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((ip, port))

def updatecoords(player_id, x, y, key, addr):

    if key == 'w' and y>1:
        y-=1
    elif key == 'a' and x>2:
        x-=2
    elif key == 's' and y<24:
        y+=1
    elif key == 'd' and x<76:
        x+=2

    updated_coords= {"player_id":str(player_id), type:"coords", "x":str(x), "y":str(y)} 
    server.sendto(updated_coords.encode(), addr)
    print(f"new coords sent {x}, {y}")
    return x, y




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

        players[playerid]=    {
                "user":f"{user}", 
                "x":f"{spawnable_x}",
                "y":f"{spawnable_y}",
                "score":0}

        updated_coords= {"player_id":str(playerid),
                          "type":"coords", 
                          "x":str(spawnable_x),
                            "y":str(spawnable_y)} 
        
        server.sendto(json.dumps(updated_coords).encode(), addr)
        


    if data["type"]=="key":

        id=int(data["playerid"])
        x=players[id]["x"]
        y=players[id]["y"]
    
        
        x, y= updatecoords(id, x, y, data["key"], addr)

        players[id]["x"]=x
        players[id]["y"]=y