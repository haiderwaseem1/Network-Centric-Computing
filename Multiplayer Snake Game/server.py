import socket
import sys
import pickle
from snake import *
import threading 
import random
import queue 

def create_socket():
    try:
        
        global host
        global port
        global skt

        host = str(sys.argv[1])
        # "10.130.38.122"
        port = int(sys.argv[2])
        
        #parameter 1 (AF_INET) = using ipv4
        #parameter 2 (SOCK_STREAM) = using TCP protocol
        skt =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error as msg:
        print ("Socket creation error: " + str(msg))


#binding socket and listening for connection from client
def bind_socket(players_number):
    try:
        global host
        global port
        global skt

        print ("Binding the Port " + str(port))

        skt.bind((host, port)) 
        skt.listen(players_number)

    except socket.error as msg:
        print ("Socket binding error: " + str(msg) + "\n" + "Retrying...")


#establish connection with client (socket must be listening)
def socket_accept(players_number):
    snake_list = []
    foodn= food()
    food_list=[]
    score_list = []

    for i in range(players_number):
        snake1 = Snake()
        color = (random.randrange(50,255), random.randrange(50,255), random.randrange(50,255))
        snake1.set_color(color)
        snake_list.append(snake1)    
        food_list.append(foodn)
        score_list.append(0)
    
    conn_list = []


    for i in range(players_number):
        conn, address = skt.accept()  #first output gives object of connection, second gives (ip address + port) of client
        print ("Connection has been established!\n" + "IP: " + address[0] + "    Port: " + str(address[1]))
        conn_list.append(conn)
    
    for i in range(players_number):
        f =  threading.Thread(target = send_info, args = (conn_list[i], snake_list,food_list,score_list, i,players_number) )
        f.start()


def send_info(conn, snake_list,food_list,score_list, snake_number,players_number):
    
    str_player_num = str(players_number)
    print(str_player_num)
    conn.send(str.encode(str_player_num))
    t = (snake_list[snake_number],food_list[snake_number])    
    conn.send(pickle.dumps(t))	
    collide = -2
    while True:
        try:
            snake_list[snake_number] = pickle.loads(conn.recv(2048))
        except:
             return
        
        conn.send(pickle.dumps(snake_list))
      
        try:
            food_list[snake_number] = pickle.loads(conn.recv(2048))
        except:
            continue

        c = 0
        for i in range(players_number):
            if food_list[i].isFoodOnScreen == False:
                print(snake_number , " ate food")
                food_list[i].spawnFood()
                food_list[i].setFoodOnScreen(True)
                c = i
            
        for j in range(players_number):
            food_list[j] = food_list[c]

        conn.send(pickle.dumps(food_list[snake_number]))

        try:
            t = pickle.loads(conn.recv(2048))
        except:
            continue

        if t[0]>=0:
            score_list[t[0]] = t[1]+1
        conn.send(pickle.dumps(score_list[snake_number]))

    conn.close()
    return

def main():

    players_number = int(sys.argv[3])

    create_socket()
    bind_socket(players_number)
    socket_accept(players_number)

main()






