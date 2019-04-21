import socket
import os
import subprocess
import pickle
import sys
from snake import *
from tkinter import messagebox


def create_connection(host, port):    
    try:
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("trying to connect")
        skt.connect((host,port))
        print ("connected")
        game(skt)
    except socket.error as msg:
        print ("Socket connection error: " + str(msg))
        
    
def game(skt):
    players_num = int(skt.recv(2048).decode())
    score = 0

    t = pickle.loads(skt.recv(2048))
    snake = t[0]
    food = t[1]
    
    g = Game()
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Snake by Haider and Zainab")
    fps = pygame.time.Clock()

    while True:  
        skt.send(pickle.dumps(snake)) 
    
        if snake.alive == False:
            messagebox.showinfo("Loser", "You have died! :( \n     Game Over")
            sys.exit()

        opponents_list = pickle.loads(skt.recv(2048))
  
        snake, food, collision = g.gameplay(snake, opponents_list, window, fps, food)

        skt.send(pickle.dumps(food))

        food = pickle.loads(skt.recv(2048))
        
        t = [collision, g.score]
        
        skt.send(pickle.dumps(t))

        g.score = pickle.loads(skt.recv(2048))
        # print ("Score: ", g.score)
       

        dead = 0
        for i in range(len(opponents_list)):
            if opponents_list[i].alive == False:
                dead += 1

        if dead == len(opponents_list) - 1:
            messagebox.showinfo("Winner", "You have won!!")
            pygame.quit()
            sys.exit()

        pygame.display.set_caption("Snake by Haider and Zainab | Score:  " + str(g.score*100))


def main(): 
    host = str(sys.argv[1])
    port = int (sys.argv[2])
    
    create_connection(host, port)


main()

