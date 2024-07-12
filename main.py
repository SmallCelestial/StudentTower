from player import *
#from steps_lib import Step_snowbiom, Floor_snowbiom

LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900

WIDTH = 1000
HEIGHT = 800

pygame.init()
main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Student_Tower")

# GLOBAL VARIABLES
main_clock = pygame.time.Clock()
game_status = "intro"  # intro, game_on, outro

# BACKGROUND_AND_FLOOR_TEXTURES
start_background = pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()

# GROUPS

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        # module responsible for background and steps display
        main_screen.blit(start_background, (0, 0))

        falling_floors_group.draw(main_screen)
        falling_floors_group.update()

        # module responsible for player animation and movement display
        player_group.draw(main_screen)
        player_group.update()

    elif game_status == "intro":
        intro = Intro(main_screen)
        intro.update()
        if intro.play_button:
            game_status = "game_on"
    elif game_status == "outro":
        pass

    pygame.display.update()
    main_clock.tick(60)  # maximum framerate 60tics = 1 second
