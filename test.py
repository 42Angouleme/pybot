import pygame
from pygame.locals import *

def main():

        pygame.init()
        pygame.mouse.set_visible(0)
        screenWidth  = pygame.display.Info().current_w
        screenHeight = pygame.display.Info().current_h
        #print(screenWidth)
        #print(screenHeight)
        size = (screenWidth, screenHeight)
        screen = pygame.display.set_mode(size)

        while True:
                for event in pygame.event.get():
                        if(event.type is pygame.FINGERDOWN):
                                x = event.x
                                y = event.y
                                print(x,y)

main()