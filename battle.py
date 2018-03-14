import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Battle in Air')
clock = pygame.time.Clock()



black=(0,0,0)


def crash():
    pass#message_display('You Crashed')


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)


        mouse= pygame.mouse.get_pos()

        #print(mouse)


        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0





    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(0,0,0)






game_intro()
game_loop()
pygame.quit()
quit()