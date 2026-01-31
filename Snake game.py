#Imports
import pygame
import copy
import random

#Initializations
'''----For Screen----'''
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
small_text = pygame.font.Font(None, 32)
title_text = pygame.font.Font(None, 64)

'''Game Stuffs'''
food = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
score = 0
alive = True
segments = []


#Class
class Snake:
    def __init__(self, x_pos, y_pos, direction, speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.direction = direction
        self.speed = speed
        self.lagpos = []
        self.eyes = [20,0,0,0]
    
    #Movement and collision detection
    def move(self, score=None, food=None,segments=None):
        alive = True
        if self.direction == 'Up':
            self.y_pos -= self.speed
        elif self.direction == 'Down':
            self.y_pos += self.speed
        elif self.direction == 'Right':
            self.x_pos += self.speed
        elif self.direction == "Left":
            self.x_pos -= self.speed
        else:
            pass

        #Check if Collided with food or segment
        for x, y in zip([self.x_pos,self.x_pos+25],[self.y_pos,self.y_pos+25]):
            if (x>food[0]-15 and x<food[0]+15 and y>food[1]-15 and y<food[1]+15):
                food = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
                score += 10
                segments.append(Snake(screen_width/2,screen_height/2,'X',5))
            for i in segments:
                if (x>i.x_pos and x<i.x_pos+15 and y>i.y_pos and y<i.y_pos+15):
                    alive = False
            if ((x>screen_width or y>screen_height) or (x<0 or y<0)):
                alive = False
            

        return alive, score, food, segments
    
    #Detect key presses
    def detect_keys(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] and self.direction!="Right"):
            self.direction = "Left"
            self.eyes = [0,0,0,20]
        elif (keys[pygame.K_s] and self.direction != "Up"):
            self.direction = "Down"
            self.eyes = [20,20,0,20]
        elif (keys[pygame.K_d] and self.direction != "Left"):
            self.direction = "Right"
            self.eyes = [20,0,20,20]
        elif (keys[pygame.K_w] and self.direction != "Down"):
            self.direction = 'Up'
            self.eyes = [0,0,20,0]
    
    #Store Lag positions
    def store_pos(self):
        self.lagpos.append([self.x_pos,self.y_pos])
        if len(self.lagpos)>4:
            del self.lagpos[0]



head = Snake(screen_width/2,screen_height/2,'X',5)

#Game Loop
run = True
while run:
    
    #Check if game has been closed or not
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    #Death
    if not alive:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            food = [random.randint(20,screen_width-20),random.randint(20,screen_height-20)]
            score = 0
            alive = True
            segments = []
            head = Snake(screen_width/2,screen_height/2,'X',5)
            alive = True

    #Snake segment positions
    if alive:
        if segments != []:
            for i in range(len(segments)-1,0,-1):
                segments[i].x_pos, segments[i].y_pos = segments[i-1].lagpos[0][0],segments[i-1].lagpos[0][1]
                segments[i].store_pos()
            segments[0].x_pos, segments[0].y_pos = head.lagpos[0][0], head.lagpos[0][1]
            segments[0].store_pos()

    #Screen
    screen.fill(0) 
    for i in segments:
       pygame.draw.rect(screen,'green',(i.x_pos,i.y_pos,25,25))

    pygame.draw.rect(screen, 'red', (food[0],food[1],15,15))
    pygame.draw.rect(screen, 'green', (head.x_pos,head.y_pos,25,25))
    
    '''Eyes'''
    eyes = head.eyes
    pygame.draw.rect(screen, 'orange', (head.x_pos+eyes[0],head.y_pos+eyes[1],5,5))
    pygame.draw.rect(screen, 'orange', (head.x_pos+eyes[2],head.y_pos+eyes[3],5,5))

    '''Texts'''
    score_text = small_text.render(f'Score: {score}', True, 'white')
    start_text = title_text.render("Press WASD to start!", True, 'white')
    death_text = title_text.render("Game over.",True,'white')
    score_text2 = small_text.render(f'Your final score was {score}!', True, 'yellow')
    death_text2 = small_text.render("Press space to reset!",True, 'white')

    if head.direction=='X':
        screen.blit(start_text,(screen_width/2-200,screen_height/2-50))
    if alive:
        screen.blit(score_text,(screen_width/2-50,10))

        '''Head'''
        head.detect_keys()
        head.store_pos()
        alive, score, food, segments = head.move(score, food, segments)
    
    else:
        screen.blit(score_text2,(screen_width/2-120,screen_height/2))
        screen.blit(death_text,(screen_width/2-120,screen_height/2-50))
        screen.blit(death_text2,(screen_width/2-110,screen_height/2+30))

    
    #Update Screen [60 Fps]
    pygame.display.update()
    clock.tick(60)