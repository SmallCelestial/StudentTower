from player import *
from steps_lib import Step_snowbiom, Floor_snowbiom

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

floor_spawn_cooldown = 60  # time between each step is spawned
floor_spawn_timer = floor_spawn_cooldown  # timer used for measuring time between spawns of steps


# GLOBAL_FUNCTIONS
def spawning_steps():  # function responsible for cyclic spawning falling steps
    global floor_spawn_timer
    global floor_spawn_cooldown
    floor_spawn_timer -= 1
    if floor_spawn_timer <= 0:
        falling_floors_group.add(Step_snowbiom())
        floor_spawn_timer = floor_spawn_cooldown


def contact_with_steps(player, steps):
    flag_1 = False
    for step in steps:
        if (step.rect.top + 5 >= player.rect.bottom >= step.rect.top - 5 and
                step.topLeft[0] <= player.rect.centerx <= step.topRight[0] and
                player.y_speed >= 0):
            player.can_jump = True
            player.rect.bottom = step.rect.top
            player.y_speed = 0
            flag_1 = True
    if not flag_1:
        player.can_jump = False


# BACKGROUND_AND_FLOOR_TEXTURES
start_background = pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()

# GROUPS
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

falling_floors_group = pygame.sprite.Group()

falling_floors_group.add(Floor_snowbiom())  # for test
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        # module responsible for background and steps display
        main_screen.blit(start_background, (0, 0))

        spawning_steps()
        falling_floors_group.draw(main_screen)
        falling_floors_group.update()

        # module responsible for player animation and movement display
        contact_with_steps(player_group.sprite, falling_floors_group)
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
