import pygame
import random #for randint

pygame.init()
main_screen=pygame.display.set_mode((1000,800)) #width,height
pygame.display.set_caption("Student_Tower")

#CLASSES
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_walk=pygame.image.load("resources/Player/player_stand.png").convert_alpha()

        self.image= self.player_walk #jakbys zmienial to napisz
        self.rect=self.image.get_rect(midbottom=(500,200)) #jakbys zmienial to napisz

        #basic_parameters
        self.x_speed=0
        self.y_speed=0
        self.current_height=0
        self.max_height=0
        floor_under_legs_status=True #if true player stands on floor and can jump


    def player_input(self):
        keys=pygame.key.get_pressed()
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]==False:
            self.y_speed=-10
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN] and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]==False:
            self.y_speed=+10
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]==False:
            self.rect.x-=5 
        if keys[pygame.K_UP]==False and keys[pygame.K_DOWN]==False and keys[pygame.K_LEFT]==False and keys[pygame.K_RIGHT]:
            self.rect.x+=5


    def gravity_function(self):
        if self.rect.bottom >= 700 and self.current_height==0:
            self.rect.bottom=700
        
        if self.y_speed<10: #max garivty strength
            self.y_speed+=0.2 #gravity strength

        self.rect.centerx+=self.x_speed
        self.rect.centery+=self.y_speed


    def update(self):
        self.player_input()
        self.gravity_function()


#CLASSES
class step_snowbiom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.floor_snowbiom_300_0=pygame.image.load('resources/floors/floor_snowbiom_300_0.png').convert_alpha()
        self.floor_snowbiom_300_1=pygame.image.load('resources/floors/floor_snowbiom_300_1.png').convert_alpha()
        self.floor_snowbiom_300_2=pygame.image.load('resources/floors/floor_snowbiom_300_2.png').convert_alpha()
        self.floor_snowbiom_300_3=pygame.image.load('resources/floors/floor_snowbiom_300_3.png').convert_alpha()
        self.floor_snowbiom_300=[self.floor_snowbiom_300_0,self.floor_snowbiom_300_1,self.floor_snowbiom_300_2,self.floor_snowbiom_300_3]
        self.floor_snowbiom_index=0
        
        
        #basic_parameters
        self.relative_height=1000 # t desribes height on screen, when =0, step disappear
        self.falling_speed=5 #1000 is at top, 0 is at bottom (contrary to y. positioning)
        self.height=50
        self.width=300

        #setting topleft adn topright points, needed for function checking if player standing on sth
        self.topLeft=[random.randint(300,600),0]
        self.topRight=[self.top_left_xy[0]+self.width,self.top_left_xy[1]]

        self.image= self.floor_snowbiom_300_0
        self.rect=self.image.get_rect(midbottom=self.top_left_xy)

        
    def falling_mechanic(self):
        self.rect.centery+=self.falling_speed
        self.relative_height-=self.falling_speed
        if self.relative_height<=0:
            self.kill()
        
        #updating topLeft and topRight cords
        self.topLeft[1]=self.relative_height #x cords, stay unchanged
        self.topRight[1]=self.relative_height #x cords, stay unchanged
        

    def animation_mehcanic(self):
        self.floor_snowbiom_index+=0.02
        if self.floor_snowbiom_index>=len(self.floor_snowbiom_300):
            self.floor_snowbiom_index=0
        self.image=self.floor_snowbiom_300[int(self.floor_snowbiom_index)]

    def update(self):
        self.falling_mechanic()
        self.animation_mehcanic()


#GLOBAL VARIABLES
main_clock=pygame.time.Clock()
game_status="game_on" #intro, game_on, outro

floor_spawn_cooldown=60 #time between each step is spawned
floor_spawn_timer=floor_spawn_cooldown #timer used for measuring time between spawns of steps

#GLOBAL_FUNCTIONS
def spawning_steps(): #function responsible for cyclic spawning falling steps
    global floor_spawn_timer
    global floor_spawn_cooldown
    floor_spawn_timer-=1
    if floor_spawn_timer<=0:
        falling_floors_group.add(step_snowbiom())
        floor_spawn_timer=floor_spawn_cooldown


def jumping_mechanic(player,steps):
    pass #TO BE IMPLEMENTED

#BACGROUND_AND_FLOOR_TEXTURES
start_background=pygame.image.load('resources/backgrounds/start_background.png').convert_alpha()
start_floor=pygame.image.load('resources/floors/start_floor.png').convert_alpha()


#GROUPS
player_group=pygame.sprite.GroupSingle()
player_group.add(Player())

falling_floors_group=pygame.sprite.Group()


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        #module reposnsible for background and steps display
        main_screen.blit(start_background,(0,0))
        main_screen.blit(start_floor,(0,700))

        spawning_steps()
        falling_floors_group.draw(main_screen)
        falling_floors_group.update()

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
