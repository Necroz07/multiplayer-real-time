import socket, json, random, time, datetime

ip = 'localhost'
port = 12345

spawnable_x, spawnable_y = 40, 15
score=""

playerid=-1
players={}
clients={}
misc={}


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((ip, port))

def updatecoords(players, playerid, key, addr, misc):

    minx, maxx= 2, 58
    miny, maxy= 1, 23

    x=int(players[playerid]["x"])
    y=int(players[playerid]["y"])

    coinx=int(misc["coinx"])
    coiny=int(misc["coiny"])

    if misc["phase"]=="finish":
        return send_state(players, playerid, addr, misc)
    

    if key == 'w' and y>miny:
        y-=1
    elif key == 'a' and x>minx:
        x-=1
    elif key == 's' and y<maxy:
        y+=1
    elif key == 'd' and x<maxx:
        x+=1


    collision=False
    scored=False
    for i in players:
        if i==playerid:
            continue
        if (x==int(players[i]["x"]) and y==int(players[i]["y"])):
            collision=True
            break

    if (x==coinx) and (y==coiny):
        
        score=int(players[playerid]["score"])
        score+=1
        players[playerid]["score"]=str(score)
        misc.pop("coinx")
        misc.pop("coiny")
        spawn_coin(players, misc)
     
    if not collision:

        players[playerid]["x"]=str(x)
        players[playerid]["y"]=str(y)

    if scored:
        spawn_coin(players, misc)

    send_state(players, playerid, addr, misc)

    



def send_state(players, playerid, addr, misc):
    msg = {"type":"state", "yourid":str(playerid), "players":players, "misc":misc}
    server.sendto((json.dumps(msg)).encode(), addr)
    

def spawn_coin(players, misc):
    x, y = initialize(players)
    misc["coinx"]=str(x)
    misc["coiny"]=str(y)



def initialize(players): 
    collision=False
    while True:
        spawnable_x= random.randint(2, 58)
        spawnable_y= random.randint(1, 23)

        for i in players:
            while (spawnable_x==players[i]["x"] and spawnable_y==players[i]["y"]):
                collision=True
                break
        
        if not collision:
            return spawnable_x, spawnable_y
                 


print("Server is listening on port 12345...")

timerend=time.time() + 120
finishend=timerend
spawn_coin(players, misc)

misc["timerend"]=str(timerend)
misc["phase"]="playing"

while True:

    if time.time() >= timerend:

        winid=max(players, key=lambda playerid: int(players[playerid]["score"]))
        misc["winner"]=str(winid)
        misc["winner_score"]=str(players[winid]["score"])
        
        spawn_coin(players, misc)
        timerend=time.time() + 120
        finishend=time.time() + 125
        misc["timerend"]=str(timerend)

        for k, val in players.items():
            val["score"]=str(0)

        misc["phase"]="finish"

    if (time.time()>=finishend):
        misc["phase"]="playing"
        misc["timerend"]=str(timerend)

    data, addr = server.recvfrom(1024)
    data = json.loads(data.decode())
    if data["type"]=="join":
        
        user = data["user"]

        playerid+=1

        spawnable_x, spawnable_y = initialize(players)

        players[playerid]= {
                            "user":f"{user}", 
                            "x":f"{spawnable_x}",
                            "y":f"{spawnable_y}",
                            "score":str(0)
                            }
        
        clients[playerid]=addr
        print("New player joined", playerid)

        send_state(players, playerid, addr, misc)
        


    if data["type"]=="key":
        print("key update recieved")
        id=int(data["playerid"])
        updatecoords(players, id, data["key"], addr, misc)



# STATE UPDATE
    if clients:

        for pid, addr in clients.items():
            send_state(players, pid, addr, misc)
            
            print("state update for", playerid)