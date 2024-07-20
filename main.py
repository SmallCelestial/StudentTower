from engine import *
from screens import Intro, Outro


LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900


pygame.init()

# GLOBAL VARIABLES
main_clock = pygame.time.Clock()
game_status = "intro"  # intro, game_on, outro


# BACKGROUND_AND_FLOOR_TEXTURES
start_background = pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()

# Engine class initialisation
main_engine = Engine(player_group, falling_floors_group)

# screens
introGroup = pygame.sprite.GroupSingle()
introGroup.add(Intro(main_screen))
intro = introGroup.sprite

# outroGroup = pygame.sprite.GroupSingle()
# outroGroup.add(Outro())
outro = Outro(main_screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif game_status == "game_on" and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_status = "outro"

    if game_status == "game_on":

        # module responsible for background and steps display
        main_screen.blit(start_background, (0, 0))

        # engine consisting of player class and various steps class
        main_engine.update()
    # TODO: remove main_screen as an argument Intro class if everything will work
    elif game_status == "intro":
        intro.update()
        introGroup.draw(main_screen)
        if intro.play_button:
            game_status = "game_on"
            intro.play_button = False
    elif game_status == "outro":
        if outro.score != main_engine.score:
            outro = Outro(main_screen, main_engine.level, main_engine.max_combo, main_engine.score)
        outro.score = main_engine.score
        outro.update()
        if outro.status == "game_on":
            main_engine.reset()
            game_status = outro.status
            outro.status = "outro"
        elif outro.status == "intro":
            main_engine.reset()
            game_status = "intro"
            outro.status = "outro"
        # TODO: The board should be reset
        # outroGroup.draw(main_screen)

    pygame.display.update()
    main_clock.tick(60)  # maximum framerate 60tics = 1 second
