import pygame
import sys
import random
import time
import tkinter
import pickle


def generate_rand_xy():
	return [50,random.randrange(1,50)*10]

def draw_objects(window, snake1, opponents_list, food):

	for pos in snake1.getBody():
		if pos[0] >= 0 and pos[1] >= 0:
			pygame.draw.rect(window, snake1.color,[pos[0], pos[1], 10, 10]) 

	for opp in opponents_list:
		for pos in opp.getBody():
			if pos[0] >= 0 and pos[1] >= 0:
				pygame.draw.rect(window, opp.color,[pos[0], pos[1], 10, 10]) 

	pygame.draw.rect(window, food.color, [food.position[0], food.position[1], 10, 10]) 


def score_update(snake, food, score):
	if (snake.move(food)==1):
		food.setFoodOnScreen(b = False)	
	return score


class Snake():
	def __init__(self):
		self.position = generate_rand_xy()
		self.alive = True
		self.color = (255,255,255)

		start_x = self.position[0]
		start_y = self.position[1]

		self.body = [[start_x, start_y], [start_x - 10, start_y], [start_x - 20, 50]]
		self.direction = "right"
		self.changeDirectionTo = self.direction

	def changeDirTo(self,dir):
		if dir == "right" and not self.direction == "left":
			self.direction = "right"
		if dir == "left" and not self.direction == "right":
			self.direction = "left"
		if dir == "up" and not self.direction == "down":
			self.direction = "up"
		if dir == "down" and not self.direction == "up":
			self.direction = "down"


	def move(self, food):
		if self.direction == "right":
			self.position[0] += 10
		if self.direction == "left":
			self.position[0] -= 10
		if self.direction == "up":
			self.position[1] -= 10
		if self.direction == "down":
			self.position[1] += 10 

		self.body.insert(0,list(self.position))

		if self.position == food.get_foodPos():
			return 1
		else:
			self.body.pop()
			return 0


	def checkCollision(self, opponents_list):
		if self.position[0] > 490 or self.position[0] < 0:
			return -1
		if self.position[1] > 490 or self.position[1] < 0:
			return -1
		for part in self.body[1:]:
			if self.position == part:
				return -1

		for i in range(len(opponents_list)):		
			for part in opponents_list[i].body:
				if self.position == part:
					return i
		return -2

	def get_command(self):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOver()
			elif event.type == pygame.KEYDOWN: #Key pressed

				if event.key == pygame.K_RIGHT:
					self.changeDirTo("right")
				if event.key == pygame.K_LEFT:
					self.changeDirTo("left")
				if event.key == pygame.K_UP:
					self.changeDirTo("up")
				if event.key == pygame.K_DOWN:
					self.changeDirTo("down")	

	def set_color(self, color):
		self.color = color

					
	def getBody(self):
		return self.body

	def kill(self):
		self.alive = False
		self.position = [-10,-10]
		self.body = [[-10,-10], [-10, -20]]


class food():
	def __init__(self):
		self.position = generate_rand_xy()
		self.isFoodOnScreen = True
		self.color = pygame.Color(0,225,0)

	def spawnFood(self):
		if self.isFoodOnScreen == False:
			self.position = generate_rand_xy()
			self.isFoodOnScreen = True
		
	def setFoodOnScreen(self,b):
		self.isFoodOnScreen = b

	def get_foodPos(self):
		return self.position

	def set_foodPos(self, new_pos):
		self.position = new_pos



class Game():
	def __init__(self):
		self.window_color = pygame.Color(0,0,0)
		self.collide = False
		self.score = 0


	def gameplay(self, snake1, opponents_list, window, fps, food):
		collision = -2
		window.fill(self.window_color)
		snake1.get_command()
		self.score = score_update(snake1, food, self.score)
		draw_objects(window, snake1, opponents_list, food)#, foodSpawner)

		if self.collide == True:
			snake1.kill()
			pygame.quit()
			return snake1, food, collision

		collision = snake1.checkCollision(opponents_list)
		if collision >= -1:
			self.collide = True
			
		pygame.display.flip() #refresh window

		fps.tick(12)

		return snake1, food, collision