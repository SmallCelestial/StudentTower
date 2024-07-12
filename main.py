import pygame
from player import *
from steps_lib import step_snowbiom

LEFT_WALL_COORDINATE = 100
RIGHT_WALL_COORDINATE = 900

pygame.init()
main_screen = pygame.display.set_mode((1000, 800)) #width,height
pygame.display.set_caption("Student_Tower")


#GLOBAL VARIABLES
main_clock = pygame.time.Clock()
game_status = "intro" #intro, game_on, outro

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

def contact_with_steps(player, steps):
        for step in steps:
            #
            if player.rect.bottom <= step.rect.top + 5 and player.rect.bottom >= step.rect.top - 5  and player.rect.centerx >= step.topLeft[0] and player.rect.centerx <= step.topRight[0] and player.y_speed >= 0:
                player.can_jump = True
                player.rect.bottom = step.rect.top
                player.y_speed = 0


#BACGROUND_AND_FLOOR_TEXTURES
start_background=pygame.image.load('resources/backgrounds/background.xcf').convert_alpha()
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
        # pygame.draw.line(main_screen, 'Black', (LEFT_WALL_COORDINATE, 700), (LEFT_WALL_COORDINATE, 0))
        # pygame.draw.line(main_screen, 'Black', (RIGHT_WALL_COORDINATE, 700), (RIGHT_WALL_COORDINATE, 0))

        #module responsible for player animation and movement display 
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
    main_clock.tick(60) #maximum framerate 60tics = 1 second
