import pygame

pygame.init()
main_screen=pygame.display.set_mode((1000,800)) #width,height
pygame.display.set_caption("Pixel_Runner")

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
        
        if self.y_speed<20:
            self.y_speed+=0.2

        self.rect.centerx+=self.x_speed
        self.rect.centery+=self.y_speed

    def update(self):
        self.player_input()
        self.gravity_function()

#GLOBAL VARIABLES
main_clock=pygame.time.Clock()
new_Variable=100
game_status="game_on" #intro, game_on, outro

#BACGROUND_AND_FLOOR_TEXTURES
start_background=pygame.image.load('resources/backgrounds/start_background.png').convert_alpha()
start_floor=pygame.image.load('resources/floors/start_floor.png').convert_alpha()

#GROUPS
player_group=pygame.sprite.GroupSingle()
player_group.add(Player())


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

    if game_status == "game_on":

        #module reposnsible for background and steps display
        main_screen.blit(start_background,(0,0))
        main_screen.blit(start_floor,(0,700))

        #module responsible for player animation and movement display 
        player_group.draw(main_screen)
        player_group.update()

    elif game_status == "intro":
        pass
    elif game_status == "outro":
        pass  

    pygame.display.update()
    main_clock.tick(60) #maximum framerate 60tics = 1 second
