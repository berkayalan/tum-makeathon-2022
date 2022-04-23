import pygame
import random
import time
import base
import leaderboard
import colours
import text
import controls



pygame.init()

def game_intro():

    # Start menu Background
    #background_image = pygame.image.load("startmenu_background.jpg").convert()
    #background_image = pygame.image.load("bakery_food.jpg").convert()
    background_image = pygame.image.load("bakery.png").convert()
    background_x = 0
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                base.quitgame()
                break

        # Start Menu Background Image
        reset_x = background_x % background_image.get_rect().width

        base.gameDisplay.blit(background_image, (reset_x - background_image.get_rect().width, 0))

        if reset_x < base.display_width:
            base.gameDisplay.blit(background_image, (reset_x, 0))

        background_x -= 1


        # base.game_loop()

        # Start Menu Buttons
        text.button(base.gameDisplay, "Play",180, 50, 200, 75, colours.white, colours.light_blue, base.game_loop)
        text.button(base.gameDisplay, "Instructions", 420, 50, 200, 75, colours.white, colours.light_blue, controls.instructions)
        text.button(base.gameDisplay, "Leaderboard", 420, 465, 200, 75, colours.white, colours.light_blue, leaderboard.display_leaderboard)
        text.button(base.gameDisplay, "Quit", 180, 465, 200, 75, colours.white, colours.light_blue, base.quitgame)

        pygame.display.update()
        base.clock.tick(45)
