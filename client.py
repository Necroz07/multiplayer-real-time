import socket, os, msvcrt, time, json

os.system("mode con: cols=85 lines=37")
ip = 'localhost'
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.settimeout(0.1)

def mapdraw(players, yourid, width=78, height=26):
    os.system('cls')
    board=""
    scoreboard=""

    for y in range(height):
        for x in range(width):

            drawn=False
            for playerid, player in players.items():
                if x==int(player["x"]) and y==int(player["y"]):
                    board+=chr(ord('A')+int(playerid))
                    drawn=True

            if not drawn:
                if x==0 or x==(width-1):
                    board+="|"
                elif y==0 or y==(height-1):
                    board+="—"
                else:
                    board+=" "
        board+="\n"

    for pid, player in players.items():
        you=""
        if yourid==pid:
            you+="(You)"
        scoreboard+=f"{player['user']} ({chr(ord('A')+int(pid))}) {you} = {player['score']}\n "
    print(board,"SCORE:\n",scoreboard, end="")
            

def sendcoords(key, playerid):
    msg = {"type":"key", "playerid":f"{playerid}", "key":f"{key}"}
    
    client.sendto(json.dumps(msg).encode(), (ip, port))

def state_extract(data):

    data=json.loads(data.decode())
    players=data["players"]
    yourid=data["yourid"]

    return players, yourid




user=input("Enter your name:\t")

join={"type":"join", "user":f"{user}"}
client.sendto(json.dumps(join).encode(), (ip, port))


data, addr = client.recvfrom(1024)

players, yourid = state_extract(data)

mapdraw(players, yourid)



while True:

    if msvcrt.kbhit():
        key = msvcrt.getch().decode("utf-8").lower()
        if key in ('w', 'a', 's', 'd'):

            sendcoords(key, yourid)

            try:
                data, addr = client.recvfrom(4096)
                players, _= state_extract(data)

            except socket.timeout:
                pass

    mapdraw(players, yourid)
    time.sleep(0.1)

    try:
        data, addr = client.recvfrom(4096)
        players, _=state_extract(data)

    except socket.timeout:
        pass