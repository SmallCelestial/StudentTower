import pygame
from player import Player
from steps_lib import step_snowbiom

pygame.init()
main_screen = pygame.display.set_mode((1000, 800)) #width,height
pygame.display.set_caption("Student_Tower")


#GLOBAL VARIABLES
main_clock = pygame.time.Clock()
game_status = "game_on" #intro, game_on, outro

floor_spawn_cooldown = 60 #time between each step is spawned
floor_spawn_timer = floor_spawn_cooldown #timer used for measuring time between spawns of steps

#GLOBAL_FUNCTIONS
def spawning_steps(): #function responsible for cyclic spawning falling steps
    global floor_spawn_timer
    global floor_spawn_cooldown
    floor_spawn_timer -= 1
    if floor_spawn_timer <= 0:
        falling_floors_group.add(step_snowbiom())
        floor_spawn_timer = floor_spawn_cooldown


def jumping_mechanic(player, steps):
    pass #TO BE IMPLEMENTED

#BACGROUND_AND_FLOOR_TEXTURES
start_background=pygame.image.load('resources/backgrounds/start_background.png').convert_alpha()
start_floor=pygame.image.load('resources/floors/start_floor.png').convert_alpha()


#GROUPS
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

falling_floors_group = pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        #module reposnsible for background and steps display
        main_screen.blit(start_background, (0, 0))
        main_screen.blit(start_floor, (0, 700))

        spawning_steps()
        falling_floors_group.draw(main_screen)
        falling_floors_group.update()

        # temporary lines imitating walls
        pygame.draw.line(main_screen, 'Black', (125, 700), (125, 0))
        pygame.draw.line(main_screen, 'Black', (875, 700), (875, 0))

        #module responsible for player animation and movement display 
        jumping_mechanic(player_group.sprite,falling_floors_group) #TO BE IMPLEMENTED
        player_group.draw(main_screen)
        player_group.update()

    elif game_status == "intro":
        pass
    elif game_status == "outro":
        pass  

    pygame.display.update()
    main_clock.tick(60) #maximum framerate 60tics = 1 second
