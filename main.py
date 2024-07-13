import pygame
from engine import *


LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900


pygame.init()

# GLOBAL VARIABLES
main_clock = pygame.time.Clock()
game_status = "game_on"  # intro, game_on, outro


# BACKGROUND_AND_FLOOR_TEXTURES
start_background = pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()
main_engine = Engine(player_group, falling_floors_group)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        # module responsible for background and steps display
        main_screen.blit(start_background, (0, 0))

        #engine consisting of player class and various steps class
        main_engine.update()

    elif game_status == "intro":
        intro = Intro(main_screen)
        intro.update()
        if intro.play_button:
            game_status = "game_on"
    elif game_status == "outro":
        pass

    pygame.display.update()
    main_clock.tick(60)  # maximum framerate 60tics = 1 second
