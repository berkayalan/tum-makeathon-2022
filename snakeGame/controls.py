import pygame
import text
import colours
import base
import startmenu

pygame.init()


def instructions():
    display = True
    box_height = 520
    box_width = 490


    instruct_image = pygame.image.load("instructions.png").convert()
    instruct_image = pygame.transform.scale(instruct_image, (480, 250))

    while display:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break


        box = pygame.surface.Surface((box_width, box_height))
        box.fill(colours.white)
        # Controls title
        titleSurf, titleRect = text.text_objects("Instructions", text.smallText, colours.black)
        titleRect.center = ((box_width/2), 50)
        box.blit(titleSurf, titleRect)

        # Instructions Text
        instructSurf2, instructRect2 = text.text_objects("Press Play and say START to begin the game!", text.smallText, colours.black)
        instructRect2.center = ((box_width/2), 105)
        box.blit(instructSurf2, instructRect2)


        # Instructions picture
        box.blit(instruct_image, (35, 175))

        # Back button
        text.button(base.gameDisplay, "Back", 50, 500, 100, 50, colours.white, colours.light_blue, startmenu.game_intro)

        pygame.draw.rect(box, colours.black, (0, 0, box_width, box_height), 3)
        base.gameDisplay.blit(box, text.center_box(box_width, box_height, base.display_width, base.display_height))
        pygame.display.update()
        pygame.time.Clock().tick(15)