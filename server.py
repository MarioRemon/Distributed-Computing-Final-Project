import socket
from _thread import *
from player import Player
import pickle

server = "10.1.0.210"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")


#players = [Player(0,0,50,50,(255,0,0)), Player(100,100, 50,50, (0,0,255))]
players = []
numOfPlayers = 0
rankers = [][2]

# # Function to send car position update to the server
# def send_position_update(position):
#     update = pickle.dumps(position)  # Serialize the position data
#     client_socket.sendall(update)
#
# # Continuously update the car position and send updates to the server
# while True:
#     # Update the car position (replace this with your own logic)
#     car_position = (x, y)  # Example position data
#
#     # Send the position update to the server
#     send_position_update(car_position)

def threaded_client(conn, playerId):
    player = Player(playerId, '', 0, 0, 0, 0, 0, len(players), 0)
    rankers.append([playerId, 0])
    print("rankooooooooooooooooooooooooooooooo")
    players.append(player)
    global numOfPlayers
    numOfPlayers += 1
    conn.send(pickle.dumps(players[playerId]))
    first3Rankers = ['Super', 'Mario', 'Remon']
    reply = ""
    reply1 = []
    while True:
        rankers.sort(key=lambda x: x[1], reverse=True)
        #rankers.reverse()
        print(rankers)
        print('2222222222222222222222222222222222222222222222222222222222222222222222222222222')
        try:
            data = pickle.loads(conn.recv(2048))
            #players[player] = data
            print('Data Received')
            print(data)
            print('########################################')

            if not data:
                print("Disconnected")
                break
            else:
                clientRequest = data.split(':', 1)

                if clientRequest[0] == '0':
                    conn.sendall(pickle.dumps(numOfPlayers))
                    print("Number of player")
                    print(len(players))
                    print('########################################')
                elif clientRequest[0] == '1':
                    print('ranks')

                    conn.send(pickle.dumps(first3Rankers))
                    print('########################################')
                elif clientRequest[0] == '2':
                        conn.send(pickle.dumps('1'))
                        print("Update the map complete")
                        player.mapComplete = clientRequest[1]
                        rankers[playerId] = int(clientRequest[1])
                        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                        print(rankers[0])
                        print("laalal")
                        print('########################################')
                        #print((player.mapComplete))
                elif clientRequest[0] == '3':
                    #players[player.update(clientRequest[1])]
                    print("Positions")
                    for value in set(players) - {playerId}:
                        print("value")
                        print(value)
                        reply1.append(value)
                        print("reply")
                        print(*reply1)
                        # reply.str(reply1)
                        # print("reply")
                        # print(reply)
                    # reply = players[player]
                    print(
                        "###################################################################################################")
                    print("Received: ", data)
                    print("Sending : ", reply1)



        # conn.sendall(pickle.dumps(len(players)))
        except:
            break
    print("Lost connection")
    conn.close()
    player.active = False
    numOfPlayers -= 1

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1