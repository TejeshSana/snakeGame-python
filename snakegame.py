import pygame
import random
import os
from sys import exit

pygame.mixer.init()

pygame.init()


#colors

white = (255,255,255)
red = (240,0,0)
black =(10,10,10) 
blue = (0,0,240)


#creating window
screen_width = 1080
screen_height = 690
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("SNAKE GAME")
pygame.display.update()


#background image for home screen
bg_img = pygame.image.load("imgs&music/logo.png")
bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height)).convert_alpha()


#background image for game over
bg_img_1 = pygame.image.load("imgs&music/game.png")
bg_img_1 = pygame.transform.scale(bg_img_1,(screen_width,screen_height)).convert_alpha()


clock = pygame.time.Clock()
font = pygame.font.SysFont('Roboto',55)


def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])



def plot_snake(gameWindow,color,snake_list,snake_size):
    for x,y in snake_list:
      pygame.draw.circle(gameWindow,color,(x,y),snake_size)

#Welcome screen

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.blit(bg_img,(0,0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    
                    game_loop()

        pygame.display.update()
        clock.tick(60)


#creating game loop
def game_loop():
    
    #creating game specific variables
    exitGame = False
    game_over =False
    snake_x =40
    snake_y = 50
    snake_size = 10
    food_size = 7
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    score=0
    food_x = random.randint(40,screen_width/2)
    food_y = random.randint(40,screen_height/2)
    fps = 45
    snake_list = []
    snake_length = 1

    #check if hiscore file exists
    if (not os.path.exists("hiscore.txt")):
        with open("imgs&music/hiscore.txt","w") as f:
            f.write("0")
    with open("imgs&music/hiscore.txt","r") as f:
       hiscore = f.read()

    while not exitGame:
        if game_over:
            with open("imgs&music/hiscore.txt","w") as f:
                 f.write(str(hiscore))
            gameWindow.blit(bg_img_1,(0,0))
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
            snake_x+=velocity_x
            snake_y+=velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                score += 10
                
                
                food_x = random.randint(40,screen_width/2)
                food_y = random.randint(40,screen_height/2)
                snake_length+=5
                if score > int(hiscore) :
                    hiscore = score

            gameWindow.fill(black)
            text_screen("   Score : "+str(score) + "                                          " + "   Hi score : "+str(hiscore),blue,5,5)
            pygame.draw.circle(gameWindow,red,(food_x,food_y),food_size)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list)>snake_length:
                del snake_list[0]
            if head in snake_list[:-1]:
                pygame.mixer.music.load('imgs&music/beep.mp3')
                pygame.mixer.music.play()
                game_over = True
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('imgs&music/beep.mp3')
                pygame.mixer.music.play()
                game_over=True
            #pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])
            plot_snake(gameWindow,white,snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    exit()

welcome()